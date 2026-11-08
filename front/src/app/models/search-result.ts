import { Document } from './document';

export interface SearchResult {
  query: string;
  count: number;
  result: Document[];
}
