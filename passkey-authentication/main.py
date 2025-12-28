"""
Passkey Authentication Backend (FIDO2/WebAuthn) using FastAPI
==============================================================

This implementation demonstrates a complete WebAuthn flow with:
- Registration Ceremony: User creates a new passkey credential
- Authentication Ceremony: User signs in with their passkey

SECURITY ARCHITECTURE:
---------------------
WebAuthn uses asymmetric cryptography (public/private key pairs):
1. During Registration:
   - Server generates a random CHALLENGE (nonce)
   - Browser/Authenticator creates a key pair
   - Private key stays on the device (never sent to server)
   - Public key + signed challenge sent to server
   - Server verifies signature and stores public key

2. During Authentication:
   - Server generates a new random CHALLENGE
   - Authenticator signs challenge with private key
   - Server verifies signature using stored public key
   - No passwords or secrets transmitted over network

This cryptographic challenge/response prevents:
- Replay attacks (each challenge is unique)
- Phishing (authenticator verifies origin)
- Password theft (no shared secrets)
- Man-in-the-middle attacks (signature verification)
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime
import secrets
import base64
import json

# WebAuthn library for FIDO2 protocol implementation
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,
    AuthenticatorTransport,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    AttestationConveyancePreference,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier

# ============================================================================
# PYDANTIC V2 MODELS - Data Validation & Storage
# ============================================================================

class UserModel(BaseModel):
    """
    User model representing a registered user.

    In production, this would be stored in a database with proper indexing.
    The user_id should be a stable, unique identifier that doesn't change.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123456",
                "username": "alice@example.com",
                "display_name": "Alice Smith",
                "created_at": "2025-12-24T10:30:00",
            }
        }
    )

    user_id: str = Field(..., description="Unique user identifier (opaque to authenticator)")
    username: str = Field(..., description="Human-readable username (email, phone, etc.)")
    display_name: str = Field(..., description="Display name shown during authentication")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    credentials: List[str] = Field(default_factory=list, description="List of credential IDs")


class CredentialModel(BaseModel):
    """
    Credential model representing a FIDO2 authenticator.

    SECURITY NOTE: The credential_public_key is the core security element.
    It's used to verify signatures during authentication. The sign_count
    helps detect credential cloning attacks.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "credential_id": "cred_abc123...",
                "user_id": "user_123456",
                "credential_public_key": "base64_encoded_public_key...",
                "sign_count": 0,
            }
        }
    )

    credential_id: str = Field(..., description="Unique credential identifier (base64url)")
    user_id: str = Field(..., description="User this credential belongs to")
    credential_public_key: bytes = Field(..., description="Public key in COSE format")
    sign_count: int = Field(default=0, description="Signature counter for clone detection")
    transports: List[str] = Field(default_factory=list, description="Transport methods (usb, nfc, ble)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    aaguid: str = Field(default="", description="Authenticator attestation GUID")


class RegistrationStartRequest(BaseModel):
    """Request to start registration ceremony"""
    username: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)


class RegistrationCompleteRequest(BaseModel):
    """Complete registration with authenticator response"""
    user_id: str
    credential: dict  # The credential response from navigator.credentials.create()


class AuthenticationStartRequest(BaseModel):
    """Request to start authentication ceremony"""
    username: str = Field(..., min_length=1, max_length=100)


class AuthenticationCompleteRequest(BaseModel):
    """Complete authentication with authenticator response"""
    username: str
    credential: dict  # The credential response from navigator.credentials.get()


# ============================================================================
# IN-MEMORY STORAGE (Production: Use PostgreSQL, MongoDB, etc.)
# ============================================================================

# Database simulation using dictionaries
users_db: Dict[str, UserModel] = {}  # username -> UserModel
credentials_db: Dict[str, CredentialModel] = {}  # credential_id -> CredentialModel
challenges_db: Dict[str, dict] = {}  # user_id/username -> challenge data

# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Passkey Authentication API",
    description="FIDO2/WebAuthn implementation for passwordless authentication",
    version="1.0.0",
)

# CORS configuration (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# CONFIGURATION - Relying Party (RP) Settings
# ============================================================================

# These settings identify your application to the authenticator
RP_ID = "localhost"  # Production: your domain (e.g., "example.com")
RP_NAME = "Passkey Auth Demo"
ORIGIN = "http://localhost:8000"  # Production: https://example.com

# ============================================================================
# REGISTRATION CEREMONY - Create New Passkey
# ============================================================================

@app.post("/api/register/start", summary="Start Registration Ceremony")
async def register_start(request: RegistrationStartRequest):
    """
    STEP 1 of REGISTRATION CEREMONY
    ================================

    This endpoint initiates passkey creation by:
    1. Creating a new user record (or retrieving existing)
    2. Generating a cryptographic CHALLENGE (random bytes)
    3. Returning PublicKeyCredentialCreationOptions to the browser

    SECURITY: The challenge is a one-time nonce that prevents replay attacks.
    The authenticator will sign this challenge along with other data.
    """

    # Check if user already exists
    if request.username in users_db:
        return JSONResponse(
            status_code=400,
            content={"error": f"User '{request.username}' already exists"}
        )

    # Create new user with unique ID
    user_id = secrets.token_urlsafe(32)  # Cryptographically secure random ID
    user = UserModel(
        user_id=user_id,
        username=request.username,
        display_name=request.display_name,
    )
    users_db[request.username] = user

    # Generate registration options with security parameters
    # The webauthn library handles the cryptographic challenge generation
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id,  # Opaque identifier (not username)
        user_name=request.username,
        user_display_name=request.display_name,

        # Cryptographic algorithm preferences (ES256 = ECDSA with SHA-256)
        # More algorithms = better compatibility with different authenticators
        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.ECDSA_SHA_256,  # Most common
            COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,  # Legacy support
            COSEAlgorithmIdentifier.ECDSA_SHA_512,
        ],

        # Attestation controls how much info about the authenticator is revealed
        # "none" = privacy-focused (default), "direct" = full attestation
        attestation=AttestationConveyancePreference.NONE,

        # Authenticator selection criteria
        authenticator_selection={
            "authenticatorAttachment": AuthenticatorAttachment.PLATFORM,  # Platform (built-in) or cross-platform (USB key)
            "residentKey": ResidentKeyRequirement.REQUIRED,  # Discoverable credential (stores username)
            "userVerification": UserVerificationRequirement.REQUIRED,  # Biometric/PIN required
        },

        # Exclude already registered credentials for this user
        exclude_credentials=[],

        # Challenge timeout (60 seconds)
        timeout=60000,
    )

    # Store the challenge for verification in step 2
    # SECURITY: We must verify that the authenticator signed THIS specific challenge
    challenges_db[user_id] = {
        "challenge": options.challenge,
        "username": request.username,
        "type": "registration",
    }

    # Convert options to JSON for the browser
    options_json = options_to_json(options)

    return JSONResponse(
        content={
            "options": json.loads(options_json),
            "user_id": user_id,
        }
    )


@app.post("/api/register/complete", summary="Complete Registration Ceremony")
async def register_complete(request: RegistrationCompleteRequest):
    """
    STEP 2 of REGISTRATION CEREMONY
    ================================

    This endpoint completes passkey creation by:
    1. Retrieving the original CHALLENGE
    2. Verifying the authenticator's response (signature + attestation)
    3. Extracting and storing the PUBLIC KEY
    4. Storing the credential for future authentication

    CRYPTOGRAPHIC VERIFICATION:
    ---------------------------
    The authenticator response contains:
    - clientDataJSON: Contains challenge, origin, type
    - attestationObject: Contains authenticator data, public key, signature

    The verification process:
    1. Checks the challenge matches what we sent
    2. Verifies the origin matches our RP_ID
    3. Validates the signature over (authenticatorData + clientDataHash)
    4. Ensures user presence (UP flag) and verification (UV flag)
    5. Extracts the credential ID and public key

    SECURITY: If any verification step fails, registration is rejected.
    """

    # Retrieve the stored challenge
    if request.user_id not in challenges_db:
        raise HTTPException(
            status_code=400,
            detail="No registration challenge found. Please start registration again."
        )

    challenge_data = challenges_db[request.user_id]
    expected_challenge = challenge_data["challenge"]
    username = challenge_data["username"]

    try:
        # Verify the registration response from the authenticator
        # This performs all cryptographic verification steps
        verification = verify_registration_response(
            credential=request.credential,
            expected_challenge=expected_challenge,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
            require_user_verification=True,  # Enforce biometric/PIN
        )

        # Extract credential details from verified response
        credential_id_base64 = base64.urlsafe_b64encode(
            verification.credential_id
        ).decode('utf-8').rstrip('=')

        # Create credential record with public key
        # SECURITY: credential_public_key is used to verify authentication signatures
        credential = CredentialModel(
            credential_id=credential_id_base64,
            user_id=request.user_id,
            credential_public_key=verification.credential_public_key,
            sign_count=verification.sign_count,
            aaguid=str(verification.aaguid),
        )

        # Store credential in database
        credentials_db[credential_id_base64] = credential

        # Link credential to user
        user = users_db.get(username)
        if user:
            user.credentials.append(credential_id_base64)

        # Clean up challenge (one-time use)
        del challenges_db[request.user_id]

        return JSONResponse(
            content={
                "verified": True,
                "message": f"Registration successful for {username}",
                "credential_id": credential_id_base64,
            }
        )

    except Exception as e:
        # Registration failed - could be tampered response, wrong challenge, etc.
        raise HTTPException(
            status_code=400,
            detail=f"Registration verification failed: {str(e)}"
        )


# ============================================================================
# AUTHENTICATION CEREMONY - Sign In with Passkey
# ============================================================================

@app.post("/api/authenticate/start", summary="Start Authentication Ceremony")
async def authenticate_start(request: AuthenticationStartRequest):
    """
    STEP 1 of AUTHENTICATION CEREMONY
    ==================================

    This endpoint initiates sign-in by:
    1. Looking up the user's registered credentials
    2. Generating a new cryptographic CHALLENGE
    3. Returning PublicKeyCredentialRequestOptions to the browser

    SECURITY: Each authentication attempt gets a fresh challenge.
    This prevents replay attacks where an attacker captures and reuses
    a previous authentication response.
    """

    # Look up user and their credentials
    user = users_db.get(request.username)
    if not user:
        # SECURITY NOTE: In production, use timing-safe error messages
        # to prevent username enumeration attacks
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user.credentials:
        raise HTTPException(
            status_code=400,
            detail="No credentials registered for this user"
        )

    # Build list of allowed credentials for this user
    # The authenticator will use one of these credentials to sign
    allowed_credentials = []
    for cred_id in user.credentials:
        cred = credentials_db.get(cred_id)
        if cred:
            allowed_credentials.append(
                PublicKeyCredentialDescriptor(
                    id=base64.urlsafe_b64decode(cred_id + "==="),  # Add padding
                    transports=[AuthenticatorTransport(t) for t in cred.transports] if cred.transports else [],
                )
            )

    # Generate authentication options with new challenge
    options = generate_authentication_options(
        rp_id=RP_ID,

        # List of credentials the user can use to authenticate
        allow_credentials=allowed_credentials,

        # Require user verification (biometric/PIN)
        user_verification=UserVerificationRequirement.REQUIRED,

        # Challenge timeout (60 seconds)
        timeout=60000,
    )

    # Store challenge for verification in step 2
    # SECURITY: We'll verify the signature was created over THIS challenge
    challenges_db[request.username] = {
        "challenge": options.challenge,
        "user_id": user.user_id,
        "type": "authentication",
    }

    # Convert options to JSON for the browser
    options_json = options_to_json(options)

    return JSONResponse(
        content={
            "options": json.loads(options_json),
        }
    )


@app.post("/api/authenticate/complete", summary="Complete Authentication Ceremony")
async def authenticate_complete(request: AuthenticationCompleteRequest):
    """
    STEP 2 of AUTHENTICATION CEREMONY
    ==================================

    This endpoint completes sign-in by:
    1. Retrieving the original CHALLENGE
    2. Looking up the credential's PUBLIC KEY
    3. Verifying the authenticator's SIGNATURE
    4. Checking the signature counter for cloning detection

    CRYPTOGRAPHIC VERIFICATION:
    ---------------------------
    The authenticator response contains:
    - clientDataJSON: Contains challenge, origin, type
    - authenticatorData: Contains RP ID hash, flags, sign count
    - signature: Digital signature over (authenticatorData + clientDataHash)

    The verification process:
    1. Retrieves the stored PUBLIC KEY for this credential
    2. Verifies the signature using the public key
    3. Checks the challenge matches what we sent
    4. Validates the origin matches our RP_ID
    5. Ensures user presence (UP flag) and verification (UV flag)
    6. Checks sign_count hasn't decreased (clone detection)

    SECURITY: Only someone with the PRIVATE KEY (on the authenticator)
    can create a valid signature. The server never sees the private key.
    """

    # Retrieve the stored challenge
    if request.username not in challenges_db:
        raise HTTPException(
            status_code=400,
            detail="No authentication challenge found. Please start authentication again."
        )

    challenge_data = challenges_db[request.username]
    expected_challenge = challenge_data["challenge"]
    user_id = challenge_data["user_id"]

    # Extract credential ID from the response
    credential_id_bytes = base64.urlsafe_b64decode(
        request.credential.get("id", "") + "==="
    )
    credential_id = base64.urlsafe_b64encode(credential_id_bytes).decode('utf-8').rstrip('=')

    # Look up the credential to get the public key
    credential = credentials_db.get(credential_id)
    if not credential:
        raise HTTPException(
            status_code=400,
            detail="Credential not found"
        )

    # Verify this credential belongs to the user
    if credential.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Credential does not belong to this user"
        )

    try:
        # Verify the authentication response using the stored public key
        # This is where the cryptographic magic happens:
        # The signature is verified using the public key, proving possession
        # of the private key without ever transmitting it.
        verification = verify_authentication_response(
            credential=request.credential,
            expected_challenge=expected_challenge,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
            credential_public_key=credential.credential_public_key,
            credential_current_sign_count=credential.sign_count,
            require_user_verification=True,
        )

        # CLONE DETECTION: Check if sign count increased
        # If an authenticator is cloned, both copies will have the same counter.
        # If one is used, its counter increments. If the other is then used,
        # its counter will be lower, indicating a potential clone.
        if verification.new_sign_count <= credential.sign_count and credential.sign_count > 0:
            # Possible cloned authenticator detected!
            raise HTTPException(
                status_code=403,
                detail="Authenticator clone detected. Please contact support."
            )

        # Update credential metadata
        credential.sign_count = verification.new_sign_count
        credential.last_used = datetime.utcnow()

        # Clean up challenge (one-time use)
        del challenges_db[request.username]

        # Authentication successful!
        # In a real application, you would:
        # 1. Create a session token (JWT, session ID, etc.)
        # 2. Set secure cookies
        # 3. Return user profile data

        return JSONResponse(
            content={
                "verified": True,
                "message": f"Authentication successful for {request.username}",
                "user": {
                    "username": request.username,
                    "display_name": users_db[request.username].display_name,
                },
            }
        )

    except Exception as e:
        # Authentication failed - invalid signature, wrong challenge, etc.
        raise HTTPException(
            status_code=401,
            detail=f"Authentication verification failed: {str(e)}"
        )


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/api/users", summary="List all users (debug only)")
async def list_users():
    """Debug endpoint to view registered users"""
    return {
        "users": [
            {
                "username": user.username,
                "display_name": user.display_name,
                "credentials_count": len(user.credentials),
                "created_at": user.created_at.isoformat(),
            }
            for user in users_db.values()
        ]
    }


@app.delete("/api/users/{username}", summary="Delete user (debug only)")
async def delete_user(username: str):
    """Debug endpoint to delete a user and their credentials"""
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete associated credentials
    for cred_id in user.credentials:
        if cred_id in credentials_db:
            del credentials_db[cred_id]

    # Delete user
    del users_db[username]

    return {"message": f"User {username} deleted successfully"}


@app.get("/", response_class=HTMLResponse, summary="Demo Frontend")
async def serve_frontend():
    """
    Minimal HTML/JavaScript frontend demonstrating WebAuthn API usage.

    This page shows:
    1. How to call navigator.credentials.create() for registration
    2. How to call navigator.credentials.get() for authentication
    3. Proper encoding/decoding of binary data (ArrayBuffer ↔ Base64)
    """
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Passkey Authentication Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        button:active {
            transform: translateY(1px);
        }
        .message {
            margin-top: 15px;
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            display: none;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .info {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            margin-top: 20px;
            font-size: 13px;
            color: #555;
        }
        .info strong {
            color: #667eea;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Passkey Authentication</h1>
        <p class="subtitle">FIDO2/WebAuthn Demo - Passwordless Login</p>

        <!-- Registration Section -->
        <div class="section">
            <h2>👤 Register New Account</h2>
            <label for="reg-username">Email or Username</label>
            <input type="text" id="reg-username" placeholder="alice@example.com" />

            <label for="reg-displayname">Display Name</label>
            <input type="text" id="reg-displayname" placeholder="Alice Smith" />

            <button onclick="register()">Create Passkey</button>
            <div id="reg-message" class="message"></div>
        </div>

        <!-- Authentication Section -->
        <div class="section">
            <h2>🔓 Sign In</h2>
            <label for="auth-username">Email or Username</label>
            <input type="text" id="auth-username" placeholder="alice@example.com" />

            <button onclick="authenticate()">Sign In with Passkey</button>
            <div id="auth-message" class="message"></div>
        </div>

        <!-- Information Panel -->
        <div class="info">
            <strong>How it works:</strong><br>
            1. Click "Create Passkey" to register using your device's biometric sensor or security key<br>
            2. Your private key stays on your device - never sent to the server<br>
            3. Sign in instantly with just a fingerprint or face scan<br>
            4. No passwords to remember or steal!
        </div>
    </div>

    <script>
        // ====================================================================
        // UTILITY FUNCTIONS - Binary Data Encoding/Decoding
        // ====================================================================

        /**
         * Converts Base64URL string to ArrayBuffer
         * WebAuthn uses ArrayBuffer, but JSON uses Base64URL strings
         */
        function base64urlToBuffer(base64url) {
            // Add padding if needed
            const padding = '='.repeat((4 - base64url.length % 4) % 4);
            const base64 = base64url.replace(/-/g, '+').replace(/_/g, '/') + padding;
            const binary = atob(base64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i);
            }
            return bytes.buffer;
        }

        /**
         * Converts ArrayBuffer to Base64URL string
         */
        function bufferToBase64url(buffer) {
            const bytes = new Uint8Array(buffer);
            let binary = '';
            for (let i = 0; i < bytes.length; i++) {
                binary += String.fromCharCode(bytes[i]);
            }
            const base64 = btoa(binary);
            return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
        }

        /**
         * Recursively converts Base64URL strings in an object to ArrayBuffers
         */
        function decodeCredentialCreationOptions(options) {
            // Convert challenge
            options.challenge = base64urlToBuffer(options.challenge);

            // Convert user.id
            options.user.id = base64urlToBuffer(options.user.id);

            // Convert excluded credentials if present
            if (options.excludeCredentials) {
                options.excludeCredentials = options.excludeCredentials.map(cred => ({
                    ...cred,
                    id: base64urlToBuffer(cred.id)
                }));
            }

            return options;
        }

        /**
         * Recursively converts Base64URL strings in authentication options
         */
        function decodeCredentialRequestOptions(options) {
            // Convert challenge
            options.challenge = base64urlToBuffer(options.challenge);

            // Convert allowed credentials if present
            if (options.allowCredentials) {
                options.allowCredentials = options.allowCredentials.map(cred => ({
                    ...cred,
                    id: base64urlToBuffer(cred.id)
                }));
            }

            return options;
        }

        /**
         * Converts PublicKeyCredential response to JSON-serializable format
         */
        function encodeCredentialResponse(credential) {
            // Extract the response data
            const response = credential.response;

            // For registration (AttestationResponse)
            if (response.attestationObject) {
                return {
                    id: credential.id,
                    rawId: bufferToBase64url(credential.rawId),
                    type: credential.type,
                    response: {
                        clientDataJSON: bufferToBase64url(response.clientDataJSON),
                        attestationObject: bufferToBase64url(response.attestationObject),
                    },
                };
            }

            // For authentication (AssertionResponse)
            if (response.authenticatorData) {
                return {
                    id: credential.id,
                    rawId: bufferToBase64url(credential.rawId),
                    type: credential.type,
                    response: {
                        clientDataJSON: bufferToBase64url(response.clientDataJSON),
                        authenticatorData: bufferToBase64url(response.authenticatorData),
                        signature: bufferToBase64url(response.signature),
                        userHandle: response.userHandle ? bufferToBase64url(response.userHandle) : null,
                    },
                };
            }

            throw new Error('Unknown credential response type');
        }

        // ====================================================================
        // REGISTRATION FLOW
        // ====================================================================

        async function register() {
            const username = document.getElementById('reg-username').value.trim();
            const displayName = document.getElementById('reg-displayname').value.trim();
            const messageEl = document.getElementById('reg-message');

            if (!username || !displayName) {
                showMessage(messageEl, 'Please fill in all fields', 'error');
                return;
            }

            try {
                // STEP 1: Request registration options from server
                // Server generates a challenge and returns credential creation options
                const startResp = await fetch('/api/register/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, display_name: displayName }),
                });

                if (!startResp.ok) {
                    const error = await startResp.json();
                    throw new Error(error.detail || error.error || 'Registration failed');
                }

                const { options, user_id } = await startResp.json();

                // STEP 2: Decode options and call WebAuthn API
                // This triggers the browser's native passkey creation UI
                const publicKeyOptions = decodeCredentialCreationOptions(options);

                console.log('Creating credential with options:', publicKeyOptions);

                // CRITICAL: This is where the browser communicates with the authenticator
                // The authenticator generates a key pair and signs the challenge
                const credential = await navigator.credentials.create({
                    publicKey: publicKeyOptions
                });

                console.log('Credential created:', credential);

                // STEP 3: Encode credential and send to server for verification
                const credentialJSON = encodeCredentialResponse(credential);

                const completeResp = await fetch('/api/register/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: user_id,
                        credential: credentialJSON,
                    }),
                });

                if (!completeResp.ok) {
                    const error = await completeResp.json();
                    throw new Error(error.detail || 'Registration verification failed');
                }

                const result = await completeResp.json();
                showMessage(messageEl, '✅ ' + result.message, 'success');

                // Clear form
                document.getElementById('reg-username').value = '';
                document.getElementById('reg-displayname').value = '';

            } catch (error) {
                console.error('Registration error:', error);
                showMessage(messageEl, '❌ ' + error.message, 'error');
            }
        }

        // ====================================================================
        // AUTHENTICATION FLOW
        // ====================================================================

        async function authenticate() {
            const username = document.getElementById('auth-username').value.trim();
            const messageEl = document.getElementById('auth-message');

            if (!username) {
                showMessage(messageEl, 'Please enter your username', 'error');
                return;
            }

            try {
                // STEP 1: Request authentication options from server
                // Server generates a new challenge and returns credential request options
                const startResp = await fetch('/api/authenticate/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username }),
                });

                if (!startResp.ok) {
                    const error = await startResp.json();
                    throw new Error(error.detail || 'Authentication failed');
                }

                const { options } = await startResp.json();

                // STEP 2: Decode options and call WebAuthn API
                // This triggers the browser's native passkey authentication UI
                const publicKeyOptions = decodeCredentialRequestOptions(options);

                console.log('Getting credential with options:', publicKeyOptions);

                // CRITICAL: This is where the browser asks the authenticator to sign
                // the challenge with the private key stored on the device
                const credential = await navigator.credentials.get({
                    publicKey: publicKeyOptions
                });

                console.log('Credential retrieved:', credential);

                // STEP 3: Encode credential and send to server for verification
                const credentialJSON = encodeCredentialResponse(credential);

                const completeResp = await fetch('/api/authenticate/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: username,
                        credential: credentialJSON,
                    }),
                });

                if (!completeResp.ok) {
                    const error = await completeResp.json();
                    throw new Error(error.detail || 'Authentication verification failed');
                }

                const result = await completeResp.json();
                showMessage(messageEl, '✅ Welcome back, ' + result.user.display_name + '!', 'success');

                // Clear form
                document.getElementById('auth-username').value = '';

            } catch (error) {
                console.error('Authentication error:', error);
                showMessage(messageEl, '❌ ' + error.message, 'error');
            }
        }

        // ====================================================================
        // UI HELPERS
        // ====================================================================

        function showMessage(element, text, type) {
            element.textContent = text;
            element.className = 'message ' + type;
            element.style.display = 'block';

            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }

        // Check WebAuthn support on page load
        window.addEventListener('load', () => {
            if (!window.PublicKeyCredential) {
                alert('⚠️ WebAuthn is not supported in this browser. Please use a modern browser like Chrome, Firefox, Safari, or Edge.');
            }
        });
    </script>
</body>
</html>
    """


@app.get("/health", summary="Health check")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "passkey-authentication",
        "version": "1.0.0",
    }


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Passkey Authentication Server (FIDO2/WebAuthn)              ║
    ║                                                              ║
    ║  API Documentation: http://localhost:8000/docs               ║
    ║  Demo Frontend:     http://localhost:8000                    ║
    ║                                                              ║
    ║  Security Features:                                          ║
    ║  ✓ Asymmetric cryptography (no shared secrets)              ║
    ║  ✓ Challenge/response prevents replay attacks               ║
    ║  ✓ Origin validation prevents phishing                      ║
    ║  ✓ User verification enforced (biometric/PIN)               ║
    ║  ✓ Signature counter for clone detection                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
