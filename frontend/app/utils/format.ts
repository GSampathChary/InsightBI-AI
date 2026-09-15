const INR_FORMATTER = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  maximumFractionDigits: 0,
});

const COMPACT_INR_FORMATTER = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  notation: 'compact',
  maximumFractionDigits: 1,
});

export const formatINR = (value?: number) => value == null ? '—' : INR_FORMATTER.format(value);

export const formatCompactINR = (value?: number) => value == null ? '—' : COMPACT_INR_FORMATTER.format(value);

export const formatIndianNumber = (value?: number) => value == null ? '—' : new Intl.NumberFormat('en-IN').format(value);
