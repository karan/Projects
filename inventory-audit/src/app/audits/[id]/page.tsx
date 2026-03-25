"use client";

import { useState } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { mockAudits } from "@/lib/mock-data";
import { formatDate, formatDateTime, getMatchRate, generateCSV } from "@/lib/utils";
import { AuditItem } from "@/types";

function DiscrepancyBadge({ discrepancy }: { discrepancy: number }) {
  if (discrepancy === 0) {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-green-700 bg-green-50 px-2.5 py-1 rounded-full">
        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
        </svg>
        Match
      </span>
    );
  }
  if (discrepancy < 0) {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-red-700 bg-red-50 px-2.5 py-1 rounded-full">
        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
        Shortage
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full">
      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
      </svg>
      Surplus
    </span>
  );
}

function DiscrepancyRow({ item }: { item: AuditItem }) {
  const hasDiscrepancy = item.discrepancy !== 0;
  return (
    <tr className={`border-b border-gray-50 hover:bg-gray-50 transition-colors ${hasDiscrepancy ? "bg-red-50/30" : ""}`}>
      <td className="px-6 py-4">
        <p className="text-sm font-medium text-gray-900">{item.productName}</p>
        <p className="text-xs text-gray-400 mt-0.5">{item.sku}</p>
      </td>
      <td className="px-6 py-4">
        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
          {item.category}
        </span>
      </td>
      <td className="px-6 py-4 text-sm text-gray-700 font-medium">
        {item.bumpaQuantity} <span className="text-xs text-gray-400 font-normal">{item.unit}</span>
      </td>
      <td className="px-6 py-4 text-sm text-gray-700 font-medium">
        {item.countedQuantity} <span className="text-xs text-gray-400 font-normal">{item.unit}</span>
      </td>
      <td className="px-6 py-4">
        {hasDiscrepancy ? (
          <span className={`text-sm font-bold ${item.discrepancy < 0 ? "text-red-600" : "text-amber-600"}`}>
            {item.discrepancy > 0 ? "+" : ""}{item.discrepancy}
          </span>
        ) : (
          <span className="text-sm text-gray-300">—</span>
        )}
      </td>
      <td className="px-6 py-4">
        <DiscrepancyBadge discrepancy={item.discrepancy} />
      </td>
    </tr>
  );
}

export default function AuditDetailPage({ params }: { params: { id: string } }) {
  const [filter, setFilter] = useState<"all" | "discrepancies">("all");
  const [downloaded, setDownloaded] = useState(false);

  const audit = mockAudits.find((a) => a.id === params.id);
  if (!audit) notFound();

  const displayItems =
    filter === "discrepancies"
      ? audit.items.filter((i) => i.discrepancy !== 0)
      : [...audit.items].sort((a, b) => {
          // discrepancies first
          if (a.discrepancy !== 0 && b.discrepancy === 0) return -1;
          if (a.discrepancy === 0 && b.discrepancy !== 0) return 1;
          return 0;
        });

  const handleDownload = () => {
    const csv = generateCSV(audit);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `bumpa-audit-${audit.date}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 3000);
  };

  const matchRate = getMatchRate(audit);
  const shortages = audit.items.filter((i) => i.discrepancy < 0);
  const surpluses = audit.items.filter((i) => i.discrepancy > 0);

  return (
    <div className="p-8">
      {/* Back */}
      <Link
        href="/audits"
        className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-900 mb-6 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Audit History
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-2xl font-bold text-gray-900">
              Audit Report &mdash; {formatDate(audit.date)}
            </h1>
            <span className="badge-completed">Completed</span>
          </div>
          <p className="text-gray-500 text-sm">
            Counted by <span className="font-medium text-gray-700">{audit.staffName}</span>
            {audit.completedAt && (
              <> &middot; Submitted {formatDateTime(audit.completedAt)}</>
            )}
          </p>
        </div>
        <button
          onClick={handleDownload}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            downloaded
              ? "bg-bumpa-green-light text-bumpa-green border border-bumpa-green/20"
              : "btn-primary"
          }`}
        >
          {downloaded ? (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Downloaded!
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download CSV
            </>
          )}
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Products</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{audit.totalProducts}</p>
        </div>
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Match Rate</p>
          <p className={`text-3xl font-bold mt-2 ${matchRate >= 90 ? "text-bumpa-green" : matchRate >= 75 ? "text-amber-500" : "text-red-500"}`}>
            {matchRate}%
          </p>
        </div>
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Shortages</p>
          <p className="text-3xl font-bold text-red-500 mt-2">{shortages.length}</p>
          <p className="text-xs text-gray-400 mt-1">Items below system count</p>
        </div>
        <div className="stat-card">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Surpluses</p>
          <p className="text-3xl font-bold text-amber-500 mt-2">{surpluses.length}</p>
          <p className="text-xs text-gray-400 mt-1">Items above system count</p>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 className="text-base font-semibold text-gray-900">Item Breakdown</h2>
          <div className="flex items-center bg-gray-100 rounded-lg p-0.5">
            <button
              onClick={() => setFilter("all")}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                filter === "all" ? "bg-white text-gray-900 shadow-sm" : "text-gray-500"
              }`}
            >
              All ({audit.totalProducts})
            </button>
            <button
              onClick={() => setFilter("discrepancies")}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                filter === "discrepancies" ? "bg-white text-gray-900 shadow-sm" : "text-gray-500"
              }`}
            >
              Discrepancies ({audit.discrepancyCount})
            </button>
          </div>
        </div>

        {displayItems.length === 0 ? (
          <div className="px-6 py-16 text-center">
            <div className="w-12 h-12 bg-bumpa-green-light rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-bumpa-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-gray-900 font-semibold">No discrepancies found</p>
            <p className="text-gray-400 text-sm mt-1">All items matched the Bumpa system count</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Product
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Category
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Bumpa Count
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Physical Count
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Difference
                  </th>
                  <th className="text-left text-xs font-semibold text-gray-400 uppercase tracking-wide px-6 py-3">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody>
                {displayItems.map((item) => (
                  <DiscrepancyRow key={item.productId} item={item} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
