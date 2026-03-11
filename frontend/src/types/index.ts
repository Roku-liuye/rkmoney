export interface Asset {
  id: number;
  name: string;
  type?: string;
  type_icon?: string;
  amount: number;
  purchase_date: string;
  sold_date?: string;
  sold_price?: number;
  daily_value: number;
  created_at: string;
  updated_at: string;
}

export interface AssetCreate {
  name: string;
  type?: string;
  type_icon?: string;
  amount: number;
  purchase_date: string;
}

export interface AssetUpdate {
  name?: string;
  type?: string;
  type_icon?: string;
  amount?: number;
  purchase_date?: string;
  sold_date?: string;
  sold_price?: number;
}

export interface AssetType {
  id: number;
  name: string;
  icon: string;
  color?: string;
  is_custom: number;
  created_at: string;
}

export interface AssetTypeCreate {
  name: string;
  icon: string;
  color?: string;
}

export interface PriceRecord {
  id: number;
  asset_id: number;
  price: number;
  date: string;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  code: number;
  data: T;
}
