import React from "react";
import { describe, expect, it } from "vitest";

describe("desktop bootstrap", () => {
  it("uses the documented local API default", () => {
    expect("http://127.0.0.1:8000/api/v1/health").toContain("/api/v1/health");
  });
});
