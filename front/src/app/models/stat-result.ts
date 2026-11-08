import { StatWord } from './stat-word';

export interface StatResult {
  total_unique_words: number;
  top_frequent_words: StatWord[];
}
