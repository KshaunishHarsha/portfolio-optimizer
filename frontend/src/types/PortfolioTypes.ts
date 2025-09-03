export interface Portfolio {
    [symbol: string]: {
      shares: number;
      price?: number;
      value?: number;
      adjusted_shares?: number;
    };
  }