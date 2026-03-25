"use client";

import { useState } from "react";
import Link from "next/link";
import { mockAudits } from "@/lib/mock-data";
import { formatDate, getMatchRate } from "@/lib/utils";
import { Audit, AuditStatus } from "@/types";

function StatusBadge({ status }: { status: Audit["status"] }) {
  if (status === "completed") return <span className="badge-completed">Completed</span>;
  if (status === "scheduled") return <span className="badge-scheduled">Scheduled</span>;
  return <span className="badge-in-progress">In Progress</span>;
}

const STATUS_FILTERS: { label: string; value: AuditStatus | "all" }[] = [
  { label: "All", value: "all" },
  { label: "Completed", value: "completed" },
  { label: "Scheduled", value: "scheduled" },
  { label: "In Progress", value: "in_progress" },
];

export default function AuditHistoryPage() {
  const [statusFilter, setStatusFilter] = useState<AuditStatus | "all">("all");
  const [search, setSearch] = useState("");

  const filtered = mockAudits.filter((audit) => {
    const matchesStatus = statusFilter === "all" || audit.status === statusFilter;
    const matchesSearch =
      search === "" ||
      audit.staffName.toLowerCase().includes(search.toLowerCase()) ||
      audit.date.includes(search);
    return matchesStatus && matchesSearch;
  });

  const completed = mockAudits.filter((a) => a.status === "completed");
  const totalDiscrepancies = completed.reduce((sum, a) => sum + a.discrepancyCount, 0);
  const avgMatchRate =
    completed.length > 0
      ? Math.round(completed.reduce((sum, a) => sum + getMatchRate(a), 0) / completed.length)
      : 0;

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Audit History</h1>
        <p className="text-gray-500 mt-1 text-sm">All inventory audits for Chidi&apos;s Store</p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Audits Completed</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{completed.length}</p>
        </div>
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Discrepancies</p>
          <p className="text-3xl font-bold text-red-500 mt-2">{totalDiscrepancies}</p>
        </div>
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Avg Match Rate</p>
          <p className="text-3xl font-bold text-bumpa-green mt-2">{avgMatchRate}%</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-5">
        {/* Search */}
        <div className="relative flex-1 max-w-xs">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search by staff or date..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-bumpa-green/30 focus:border-bumpa-green"
          />
        </div>

        {/* Status filter tabs */}
        <div className="flex items-center bg-white border border-gray-200 rounded-lg p-0.5">
          {STATUS_FILTERS.map((f) => (
            <button
              key={f.value}
              onClick={() => setStatusFilter(f.value)}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                statusFilter === f.value
                  ? "bg-bumpa-green text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-100">
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Date
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Staff
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Frequency
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Products
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Discrepancies
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Match Rate
              </th>
              <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                Status
              </th>
              <th className="px-6 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-6 py-12 text-center text-gray-400 text-sm">
                  No audits found
                </td>
              </tr>
            ) : (
              filtered.map((audit) => (
                <tr key={audit.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {formatDate(audit.date)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{audit.staffName}</td>
                  <td className="px-6 py-4">
                    <span className="text-xs font-medium text-gray-500 capitalize bg-gray-100 px-2 py-1 rounded">
                      {audit.frequency}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{audit.totalProducts}</td>
                  <td className="px-6 py-4">
                    {audit.status === "scheduled" ? (
                      <span className="text-gray-400 text-sm">—</span>
                    ) : audit.discrepancyCount > 0 ? (
                      <span className="text-sm font-semibold text-red-500">
                        {audit.discrepancyCount}
                      </span>
                    ) : (
                      <span className="text-sm font-semibold text-bumpa-green">None</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {audit.status === "scheduled" ? (
                      <span className="text-gray-400">—</span>
                    ) : (
                      <span
                        className={
                          getMatchRate(audit) === 100
                            ? "text-bumpa-green font-semibold"
                            : getMatchRate(audit) >= 90
                            ? "text-amber-500 font-semibold"
                            : "text-red-500 font-semibold"
                        }
                      >
                        {getMatchRate(audit)}%
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={audit.status} />
                  </td>
                  <td className="px-6 py-4">
                    {audit.status !== "scheduled" && (
                      <Link
                        href={`/audits/${audit.id}`}
                        className="text-bumpa-green text-sm font-medium hover:underline"
                      >
                        View Report
                      </Link>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
