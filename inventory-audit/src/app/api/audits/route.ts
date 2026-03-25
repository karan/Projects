import { NextResponse } from "next/server";
import { mockAudits } from "@/lib/mock-data";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const limit = searchParams.get("limit");

  let audits = [...mockAudits];

  if (status && status !== "all") {
    audits = audits.filter((a) => a.status === status);
  }

  if (limit) {
    audits = audits.slice(0, parseInt(limit));
  }

  // Strip items for list view to keep payload light
  const summary = audits.map(({ items: _, ...rest }) => rest);

  return NextResponse.json({ audits: summary, total: summary.length });
}
