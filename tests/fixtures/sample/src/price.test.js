import { describe, expect, it } from "vitest";
import { applyDiscount, splitTotal } from "./price.js";

describe("applyDiscount", () => {
  it("applies a percentage discount", () => {
    expect(applyDiscount(19.99, 15)).toBe(16.99);
  });

  it("returns the full price for 0%", () => {
    expect(applyDiscount(10, 0)).toBe(10);
  });

  it("rejects discounts over 100%", () => {
    expect(() => applyDiscount(10, 120)).toThrow(RangeError);
  });
});

describe("splitTotal", () => {
  it("splits evenly", () => {
    expect(splitTotal(99, 3)).toEqual([33, 33, 33]);
  });
});
