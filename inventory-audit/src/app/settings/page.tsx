"use client";

import { useState } from "react";
import { mockSettings } from "@/lib/mock-data";
import { getNextAuditDate } from "@/lib/utils";
import { AuditFrequency } from "@/types";

const FREQUENCY_OPTIONS: {
  value: AuditFrequency;
  label: string;
  description: string;
  icon: React.ReactNode;
}[] = [
  {
    value: "daily",
    label: "Daily",
    description: "Best for high-volume stores with fast-moving stock",
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    ),
  },
  {
    value: "weekly",
    label: "Weekly",
    description: "Great balance for most retail stores — audits every 7 days",
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
  },
  {
    value: "monthly",
    label: "Monthly",
    description: "Ideal for low-turnover businesses or small inventories",
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
];

export default function SettingsPage() {
  const [frequency, setFrequency] = useState<AuditFrequency>(mockSettings.frequency);
  const [email, setEmail] = useState(mockSettings.notifyEmail);
  const [reminder, setReminder] = useState(mockSettings.reminderEnabled);
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const nextDate = getNextAuditDate(frequency);

  const handleSave = async () => {
    setSaving(true);
    // Simulate API call
    await new Promise((r) => setTimeout(r, 800));
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Audit Settings</h1>
        <p className="text-gray-500 mt-1 text-sm">
          Configure how often your inventory should be audited
        </p>
      </div>

      {/* Frequency Picker */}
      <section className="mb-8">
        <h2 className="text-sm font-semibold text-gray-900 mb-1">Audit Frequency</h2>
        <p className="text-sm text-gray-500 mb-4">
          How often should your staff count physical stock?
        </p>
        <div className="space-y-3">
          {FREQUENCY_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setFrequency(opt.value)}
              className={`w-full flex items-center gap-4 p-4 rounded-xl border-2 text-left transition-all ${
                frequency === opt.value
                  ? "border-bumpa-green bg-bumpa-green-light"
                  : "border-gray-200 bg-white hover:border-gray-300"
              }`}
            >
              <div
                className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
                  frequency === opt.value
                    ? "bg-bumpa-green text-white"
                    : "bg-gray-100 text-gray-500"
                }`}
              >
                {opt.icon}
              </div>
              <div className="flex-1">
                <p
                  className={`font-semibold text-sm ${
                    frequency === opt.value ? "text-bumpa-green" : "text-gray-900"
                  }`}
                >
                  {opt.label}
                </p>
                <p className="text-xs text-gray-500 mt-0.5">{opt.description}</p>
              </div>
              <div
                className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                  frequency === opt.value
                    ? "border-bumpa-green bg-bumpa-green"
                    : "border-gray-300"
                }`}
              >
                {frequency === opt.value && (
                  <div className="w-2 h-2 rounded-full bg-white" />
                )}
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Next Audit Preview */}
      <div className="bg-bumpa-green-light border border-bumpa-green/20 rounded-xl p-4 mb-8 flex items-center gap-3">
        <svg className="w-5 h-5 text-bumpa-green flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-sm text-bumpa-green">
          With <strong>{frequency}</strong> audits, your next audit will be scheduled for{" "}
          <strong>
            {new Date(nextDate).toLocaleDateString("en-NG", {
              weekday: "long",
              day: "numeric",
              month: "long",
              year: "numeric",
            })}
          </strong>
        </p>
      </div>

      {/* Notifications */}
      <section className="mb-8">
        <h2 className="text-sm font-semibold text-gray-900 mb-1">Notifications</h2>
        <p className="text-sm text-gray-500 mb-4">
          Where should audit reports be sent?
        </p>

        <div className="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              Report Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="owner@yourbusiness.com"
              className="w-full px-3 py-2.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-bumpa-green/30 focus:border-bumpa-green transition-colors"
            />
            <p className="text-xs text-gray-400 mt-1.5">
              You&apos;ll receive a PDF report after every completed audit
            </p>
          </div>

          {/* Reminder toggle */}
          <div className="flex items-center justify-between pt-2 border-t border-gray-100">
            <div>
              <p className="text-sm font-medium text-gray-900">Audit Reminders</p>
              <p className="text-xs text-gray-400 mt-0.5">
                Get reminded 24 hours before a scheduled audit
              </p>
            </div>
            <button
              onClick={() => setReminder((r) => !r)}
              className={`relative w-11 h-6 rounded-full transition-colors ${
                reminder ? "bg-bumpa-green" : "bg-gray-200"
              }`}
            >
              <span
                className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                  reminder ? "translate-x-5" : "translate-x-0"
                }`}
              />
            </button>
          </div>
        </div>
      </section>

      {/* Save Button */}
      <div className="flex items-center gap-3">
        <button
          onClick={handleSave}
          disabled={saving}
          className={`btn-primary flex items-center gap-2 ${saving ? "opacity-70 cursor-not-allowed" : ""}`}
        >
          {saving ? (
            <>
              <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Saving...
            </>
          ) : saved ? (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Saved!
            </>
          ) : (
            "Save Settings"
          )}
        </button>
        {saved && (
          <p className="text-sm text-bumpa-green">Settings updated successfully</p>
        )}
      </div>
    </div>
  );
}
