import { NextResponse } from "next/server";
import { mockSettings } from "@/lib/mock-data";
import { AuditFrequency } from "@/types";

// In-memory store for mock — resets on server restart
let currentSettings = { ...mockSettings };

export async function GET() {
  return NextResponse.json({ settings: currentSettings });
}

export async function POST(request: Request) {
  const body = await request.json();

  const { frequency, notifyEmail, reminderEnabled } = body as {
    frequency?: AuditFrequency;
    notifyEmail?: string;
    reminderEnabled?: boolean;
  };

  if (frequency && !["daily", "weekly", "monthly"].includes(frequency)) {
    return NextResponse.json({ error: "Invalid frequency" }, { status: 400 });
  }

  currentSettings = {
    ...currentSettings,
    ...(frequency && { frequency }),
    ...(notifyEmail !== undefined && { notifyEmail }),
    ...(reminderEnabled !== undefined && { reminderEnabled }),
  };

  return NextResponse.json({ settings: currentSettings, success: true });
}
