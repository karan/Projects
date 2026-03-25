import Link from "next/link";
import { mockAudits, mockSettings } from "@/lib/mock-data";
import { formatDate, getMatchRate, getDaysUntil } from "@/lib/utils";
import { Audit } from "@/types";

function StatusBadge({ status }: { status: Audit["status"] }) {
  if (status === "completed") return <span className="badge-completed">Completed</span>;
  if (status === "scheduled") return <span className="badge-scheduled">Scheduled</span>;
  return <span className="badge-in-progress">In Progress</span>;
}

export default function Dashboard() {
  const completedAudits = mockAudits.filter((a) => a.status === "completed");
  const lastAudit = completedAudits[0];
  const recentAudits = mockAudits.slice(0, 4);

  const avgDiscrepancyRate =
    completedAudits.length > 0
      ? Math.round(
          completedAudits.reduce(
            (sum, a) => sum + (a.discrepancyCount / a.totalProducts) * 100,
            0
          ) / completedAudits.length
        )
      : 0;

  const daysUntilNext = getDaysUntil(mockSettings.nextAuditDate);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Good morning, Chidi</h1>
        <p className="text-gray-500 mt-1 text-sm">
          Wednesday, 25 March 2026 &nbsp;&middot;&nbsp; Inventory Audit Dashboard
        </p>
      </div>

      {/* Next Audit Banner */}
      <div className="bg-bumpa-green rounded-xl p-5 mb-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <p className="text-white/80 text-sm font-medium">Next Scheduled Audit</p>
            <p className="text-white text-xl font-bold">
              {formatDate(mockSettings.nextAuditDate)}
            </p>
            <p className="text-white/70 text-sm mt-0.5">
              {daysUntilNext === 0
                ? "Today"
                : daysUntilNext === 1
                ? "Tomorrow"
                : `In ${daysUntilNext} days`}{" "}
              &middot; {mockSettings.frequency.charAt(0).toUpperCase() + mockSettings.frequency.slice(1)} audit
            </p>
          </div>
        </div>
        <Link
          href="/settings"
          className="bg-white/20 hover:bg-white/30 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          Change Schedule
        </Link>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Audits</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{completedAudits.length}</p>
          <p className="text-xs text-gray-400 mt-1">All time</p>
        </div>

        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Avg Match Rate</p>
          <p className="text-3xl font-bold text-bumpa-green mt-2">
            {100 - avgDiscrepancyRate}%
          </p>
          <p className="text-xs text-gray-400 mt-1">Across all audits</p>
        </div>

        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Last Audit</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {lastAudit ? getMatchRate(lastAudit) : 0}%
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {lastAudit ? formatDate(lastAudit.date) : "No audits yet"}
          </p>
        </div>

        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Products Tracked</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">12</p>
          <p className="text-xs text-gray-400 mt-1">Synced from Bumpa</p>
        </div>
      </div>

      {/* Last Audit Summary */}
      {lastAudit && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm mb-6">
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <div>
              <h2 className="text-base font-semibold text-gray-900">Last Audit Summary</h2>
              <p className="text-sm text-gray-400 mt-0.5">
                {formatDate(lastAudit.date)} &middot; Counted by {lastAudit.staffName}
              </p>
            </div>
            <Link href={`/audits/${lastAudit.id}`} className="btn-secondary">
              View Full Report
            </Link>
          </div>

          <div className="px-6 py-4 grid grid-cols-3 gap-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{lastAudit.totalProducts}</p>
              <p className="text-xs text-gray-500 mt-1">Products Counted</p>
            </div>
            <div className="text-center border-x border-gray-100">
              <p className="text-2xl font-bold text-red-500">{lastAudit.discrepancyCount}</p>
              <p className="text-xs text-gray-500 mt-1">Discrepancies Found</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-bumpa-green">{getMatchRate(lastAudit)}%</p>
              <p className="text-xs text-gray-500 mt-1">Match Rate</p>
            </div>
          </div>

          {/* Top discrepancies */}
          {lastAudit.items.filter((i) => i.discrepancy !== 0).length > 0 && (
            <div className="px-6 pb-4">
              <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Discrepancies
              </p>
              <div className="space-y-2">
                {lastAudit.items
                  .filter((item) => item.discrepancy !== 0)
                  .map((item) => (
                    <div
                      key={item.productId}
                      className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2.5"
                    >
                      <div>
                        <p className="text-sm font-medium text-gray-900">{item.productName}</p>
                        <p className="text-xs text-gray-400">{item.sku}</p>
                      </div>
                      <div className="text-right">
                        <span
                          className={`text-sm font-bold ${
                            item.discrepancy < 0 ? "text-red-500" : "text-amber-500"
                          }`}
                        >
                          {item.discrepancy > 0 ? "+" : ""}{item.discrepancy} {item.unit}
                        </span>
                        <p className="text-xs text-gray-400">
                          {item.discrepancy < 0 ? "Shortage" : "Surplus"}
                        </p>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Recent Audits Table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 className="text-base font-semibold text-gray-900">Recent Audits</h2>
          <Link href="/audits" className="text-bumpa-green text-sm font-medium hover:underline">
            View all
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-50">
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                  Date
                </th>
                <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                  Staff
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
              {recentAudits.map((audit) => (
                <tr key={audit.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {formatDate(audit.date)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{audit.staffName}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{audit.totalProducts}</td>
                  <td className="px-6 py-4">
                    {audit.discrepancyCount > 0 ? (
                      <span className="text-sm font-medium text-red-500">
                        {audit.discrepancyCount}
                      </span>
                    ) : (
                      <span className="text-sm text-gray-400">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {audit.status === "scheduled" ? (
                      <span className="text-gray-400">—</span>
                    ) : (
                      <span className={getMatchRate(audit) === 100 ? "text-bumpa-green font-medium" : "text-gray-700"}>
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
                        View
                      </Link>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
