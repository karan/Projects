import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "Bumpa Inventory Audit",
  description: "Track, count, and reconcile your inventory with Bumpa",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-60 min-h-screen">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
