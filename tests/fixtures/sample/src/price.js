export function applyDiscount(price, percent) {
  if (percent < 0 || percent > 100) {
    throw new RangeError("percent must be between 0 and 100");
  }
  return Math.round(price * (100 - percent)) / 100;
}

export function splitTotal(total, people) {
  const share = Math.floor((total * 100) / people) / 100;
  return Array.from({ length: people }, () => share);
}
