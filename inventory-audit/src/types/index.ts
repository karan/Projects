export type AuditFrequency = "daily" | "weekly" | "monthly";
export type AuditStatus = "completed" | "in_progress" | "scheduled";

export interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  bumpaQuantity: number;
  unit: string;
}

export interface AuditItem {
  productId: string;
  productName: string;
  sku: string;
  category: string;
  bumpaQuantity: number;
  countedQuantity: number;
  discrepancy: number; // countedQuantity - bumpaQuantity
  unit: string;
}

export interface Audit {
  id: string;
  date: string; // ISO date string
  frequency: AuditFrequency;
  staffName: string;
  status: AuditStatus;
  items: AuditItem[];
  totalProducts: number;
  discrepancyCount: number;
  completedAt?: string;
}

export interface AuditSettings {
  frequency: AuditFrequency;
  nextAuditDate: string;
  notifyEmail: string;
  reminderEnabled: boolean;
}
