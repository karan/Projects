# 🔐 Passkey Authentication Backend (FIDO2/WebAuthn)

A production-ready backend prototype implementing **Passkey Authentication** using FastAPI and the WebAuthn protocol. This demonstrates passwordless authentication with biometric sensors, security keys, and platform authenticators.

## 🎯 Features

### Security Architecture
- **Asymmetric Cryptography**: Public/private key pairs (no shared secrets)
- **Challenge/Response Flow**: Cryptographic proofs prevent replay attacks
- **Origin Validation**: Prevents phishing attacks
- **User Verification**: Enforces biometric or PIN authentication
- **Clone Detection**: Signature counters detect credential duplication

### Implementation Highlights
- ✅ Clean separation of **Registration** and **Authentication** ceremonies
- ✅ Pydantic V2 models for type-safe data validation
- ✅ In-memory database (easy to swap for PostgreSQL/MongoDB)
- ✅ Comprehensive security documentation in code comments
- ✅ Minimal HTML/JS frontend demonstrating `navigator.credentials` API
- ✅ RESTful API with automatic OpenAPI documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Modern browser (Chrome, Firefox, Safari, Edge)
- HTTPS or localhost (WebAuthn requirement)

### Installation

```bash
# Clone or navigate to the project directory
cd passkey-authentication

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The server will start at:
- **Frontend Demo**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 How It Works

### Registration Ceremony (Create Passkey)

```
┌─────────┐                  ┌─────────┐                  ┌──────────────┐
│ Browser │                  │  Server │                  │ Authenticator│
└────┬────┘                  └────┬────┘                  └──────┬───────┘
     │                            │                               │
     │ 1. POST /api/register/start│                               │
     │ ──────────────────────────>│                               │
     │                            │                               │
     │    2. Generate Challenge   │                               │
     │                            │ (random bytes)                │
     │                            │                               │
     │ 3. Return CreationOptions  │                               │
     │ <──────────────────────────│                               │
     │                            │                               │
     │ 4. navigator.credentials.create()                          │
     │ ───────────────────────────────────────────────────────────>│
     │                            │                               │
     │                            │    5. Generate Key Pair       │
     │                            │       (Private key stays      │
     │                            │        on device!)            │
     │                            │                               │
     │ 6. Return Public Key + Signed Challenge                    │
     │ <───────────────────────────────────────────────────────────│
     │                            │                               │
     │ 7. POST /api/register/complete                             │
     │    (public key, signature) │                               │
     │ ──────────────────────────>│                               │
     │                            │                               │
     │                            │ 8. Verify Signature           │
     │                            │    Store Public Key           │
     │                            │                               │
     │ 9. Success Response        │                               │
     │ <──────────────────────────│                               │
```

### Authentication Ceremony (Sign In)

```
┌─────────┐                  ┌─────────┐                  ┌──────────────┐
│ Browser │                  │  Server │                  │ Authenticator│
└────┬────┘                  └────┬────┘                  └──────┬───────┘
     │                            │                               │
     │ 1. POST /api/authenticate/start                            │
     │ ──────────────────────────>│                               │
     │                            │                               │
     │    2. Generate Challenge   │                               │
     │                            │ (new random bytes)            │
     │                            │                               │
     │ 3. Return RequestOptions   │                               │
     │ <──────────────────────────│                               │
     │                            │                               │
     │ 4. navigator.credentials.get()                             │
     │ ───────────────────────────────────────────────────────────>│
     │                            │                               │
     │                            │    5. Sign Challenge          │
     │                            │       (with private key)      │
     │                            │                               │
     │ 6. Return Signature                                        │
     │ <───────────────────────────────────────────────────────────│
     │                            │                               │
     │ 7. POST /api/authenticate/complete                         │
     │    (signature)             │                               │
     │ ──────────────────────────>│                               │
     │                            │                               │
     │                            │ 8. Verify Signature           │
     │                            │    (using stored public key)  │
     │                            │    Check sign counter         │
     │                            │                               │
     │ 9. Success Response        │                               │
     │    (session token)         │                               │
     │ <──────────────────────────│                               │
```

## 🔬 Cryptographic Challenge/Response Flow

### Why Challenge/Response?

Traditional password authentication sends the secret (password) to the server. With WebAuthn:
1. **Server generates a random challenge** (nonce) - a one-time value
2. **Authenticator signs the challenge** with the private key
3. **Server verifies the signature** using the stored public key

**Key Properties:**
- ✅ **Private key never leaves the device** - no secret to steal
- ✅ **Each challenge is unique** - prevents replay attacks
- ✅ **Origin is cryptographically bound** - prevents phishing
- ✅ **User presence verified** - requires physical interaction

### Signature Verification Process

```python
# During Registration:
signature = sign(private_key, challenge + authenticator_data + client_data)
# Server stores: public_key

# During Authentication:
signature = sign(private_key, new_challenge + authenticator_data + client_data)
verified = verify(public_key, signature, new_challenge + authenticator_data + client_data)
# If verified == True, user is authenticated!
```

### Clone Detection

Each authenticator maintains a **signature counter** that increments with each use:
- If counter **increases**: Normal usage
- If counter **decreases or stays same**: Possible cloned credential
- Server can **lock the account** if clone detected

## 🏗️ Project Structure

```
passkey-authentication/
├── main.py              # Complete FastAPI backend
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Code Organization

```python
# main.py Structure:
├── Pydantic V2 Models
│   ├── UserModel          # User entity
│   ├── CredentialModel    # Stored passkey credentials
│   └── Request/Response models
│
├── In-Memory Storage
│   ├── users_db           # username -> UserModel
│   ├── credentials_db     # credential_id -> CredentialModel
│   └── challenges_db      # Temporary challenge storage
│
├── Registration Ceremony
│   ├── POST /api/register/start     # Generate challenge
│   └── POST /api/register/complete  # Verify and store
│
├── Authentication Ceremony
│   ├── POST /api/authenticate/start     # Generate challenge
│   └── POST /api/authenticate/complete  # Verify signature
│
└── Frontend
    └── GET /                # Minimal HTML/JS demo
```

## 📡 API Endpoints

### Registration

#### `POST /api/register/start`
Start registration ceremony and get challenge.

**Request:**
```json
{
  "username": "alice@example.com",
  "display_name": "Alice Smith"
}
```

**Response:**
```json
{
  "options": {
    "rp": { "id": "localhost", "name": "Passkey Auth Demo" },
    "user": { "id": "...", "name": "alice@example.com", "displayName": "Alice Smith" },
    "challenge": "base64url_encoded_challenge",
    "pubKeyCredParams": [...]
  },
  "user_id": "unique_user_id"
}
```

#### `POST /api/register/complete`
Complete registration with authenticator response.

**Request:**
```json
{
  "user_id": "unique_user_id",
  "credential": {
    "id": "credential_id",
    "rawId": "base64url_encoded",
    "response": {
      "clientDataJSON": "base64url_encoded",
      "attestationObject": "base64url_encoded"
    }
  }
}
```

### Authentication

#### `POST /api/authenticate/start`
Start authentication and get challenge.

**Request:**
```json
{
  "username": "alice@example.com"
}
```

**Response:**
```json
{
  "options": {
    "challenge": "base64url_encoded_challenge",
    "allowCredentials": [...],
    "userVerification": "required"
  }
}
```

#### `POST /api/authenticate/complete`
Complete authentication with signature.

**Request:**
```json
{
  "username": "alice@example.com",
  "credential": {
    "id": "credential_id",
    "rawId": "base64url_encoded",
    "response": {
      "clientDataJSON": "base64url_encoded",
      "authenticatorData": "base64url_encoded",
      "signature": "base64url_encoded"
    }
  }
}
```

## 🧪 Testing the Implementation

### Manual Testing

1. **Open browser**: Navigate to http://localhost:8000
2. **Register**:
   - Enter username and display name
   - Click "Create Passkey"
   - Follow your device's biometric prompt
3. **Authenticate**:
   - Enter the same username
   - Click "Sign In with Passkey"
   - Verify with biometric

### Using API Docs

Visit http://localhost:8000/docs for interactive API testing with Swagger UI.

### Programmatic Testing

```python
import requests

# Register
start_resp = requests.post('http://localhost:8000/api/register/start', json={
    'username': 'test@example.com',
    'display_name': 'Test User'
})
# ... continue with WebAuthn flow ...
```

## 🔒 Security Considerations

### Production Deployment

Before deploying to production, consider:

1. **HTTPS Required**: WebAuthn only works over HTTPS (except localhost)
   ```python
   RP_ID = "example.com"  # Your domain
   ORIGIN = "https://example.com"
   ```

2. **Database**: Replace in-memory storage with persistent database
   ```python
   # Use PostgreSQL, MongoDB, etc.
   # Add proper indexing on user_id and credential_id
   ```

3. **Session Management**: Implement proper session tokens
   ```python
   # After successful authentication:
   - Generate JWT or session token
   - Set secure, httpOnly cookies
   - Implement token refresh logic
   ```

4. **Rate Limiting**: Prevent brute force attacks
   ```python
   from slowapi import Limiter
   # Limit registration/authentication attempts
   ```

5. **CORS**: Restrict allowed origins
   ```python
   allow_origins=["https://example.com"]  # Not ["*"]
   ```

6. **Attestation**: For high-security scenarios, use attestation
   ```python
   attestation=AttestationConveyancePreference.DIRECT
   # Verify authenticator is trusted
   ```

7. **User Enumeration**: Use timing-safe error messages
   ```python
   # Don't reveal if username exists
   # Return generic "Invalid credentials" message
   ```

### Threat Model

This implementation defends against:
- ✅ **Password theft**: No passwords used
- ✅ **Phishing**: Origin validation
- ✅ **Replay attacks**: One-time challenges
- ✅ **Man-in-the-middle**: Signature verification
- ✅ **Credential stuffing**: No shared secrets
- ✅ **Social engineering**: Requires physical device

Does NOT defend against:
- ❌ **Device theft**: If device is unlocked/compromised
- ❌ **Malware on client**: Could capture biometric or intercept
- ❌ **Server compromise**: Attacker could modify code

## 📚 Learn More

### WebAuthn Resources
- [WebAuthn Specification](https://www.w3.org/TR/webauthn-2/)
- [FIDO Alliance](https://fidoalliance.org/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API)

### Library Documentation
- [py_webauthn](https://github.com/duo-labs/py_webauthn)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)

## 🛠️ Customization

### Change Authenticator Type

```python
# Platform authenticators (built-in: Face ID, Touch ID, Windows Hello)
authenticator_selection={
    "authenticatorAttachment": AuthenticatorAttachment.PLATFORM,
}

# Cross-platform authenticators (USB security keys: YubiKey, etc.)
authenticator_selection={
    "authenticatorAttachment": AuthenticatorAttachment.CROSS_PLATFORM,
}

# Allow both
authenticator_selection={
    # Don't specify authenticatorAttachment
}
```

### Adjust User Verification

```python
# Required (biometric/PIN always needed)
user_verification=UserVerificationRequirement.REQUIRED

# Preferred (use if available)
user_verification=UserVerificationRequirement.PREFERRED

# Discouraged (presence only, no biometric)
user_verification=UserVerificationRequirement.DISCOURAGED
```

### Add Database Integration

```python
# Example with SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    # ... other fields

class Credential(Base):
    __tablename__ = 'credentials'
    credential_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    credential_public_key = Column(LargeBinary)
    # ... other fields
```

## 🤝 Contributing

This is a prototype for educational purposes. For production use:
1. Add comprehensive error handling
2. Implement database persistence
3. Add session management
4. Include rate limiting
5. Add logging and monitoring
6. Write unit and integration tests
7. Implement account recovery flows

## 📄 License

MIT License - Feel free to use this code for learning and production projects.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [py_webauthn](https://github.com/duo-labs/py_webauthn) - WebAuthn implementation
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Built with security in mind** 🔒 **No passwords, no problems** 🎉
