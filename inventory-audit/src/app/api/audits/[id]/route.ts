import { NextResponse } from "next/server";
import { mockAudits } from "@/lib/mock-data";

export async function GET(
  _request: Request,
  { params }: { params: { id: string } }
) {
  const audit = mockAudits.find((a) => a.id === params.id);

  if (!audit) {
    return NextResponse.json({ error: "Audit not found" }, { status: 404 });
  }

  return NextResponse.json({ audit });
}
