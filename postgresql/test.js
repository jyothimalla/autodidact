 /*
AI: Certainly! You can cache the tax calculation using the useCallback() hook. Here’s how you can do it:
*/

import React, { useState, useCallback } from "react";

const TAX_BANDS = [
  { limit: 12570, rate: 0 },
  { limit: 50270, rate: 0.2 },
  { limit: 125140, rate: 0.4 },
  { limit: Infinity, rate: 0.45 },
];

function simulateHeavyTaxCalculation(income) {
  let tax = 0;
  let previousLimit = 0;

  for (const band of TAX_BANDS) {
    if (income > band.limit) {
      tax += (band.limit - previousLimit) * band.rate;
      previousLimit = band.limit;
    } else {
      tax += (income - previousLimit) * band.rate;
      break;
    }
  }

  // Simulated delay of future problems
  for (let i = 0; i < 1e7; i++) {}

  return tax;
}

export default function TaxCalculator() {
  const [income, setIncome] = useState(0);
  const [calculatedTax, setCalculatedTax] = useState(0);

  // Memoize the function itself, so it's stable across re-renders
  const calculateTax = useCallback((income) => {
    return simulateHeavyTaxCalculation(income);
  }, []);

  const handleCalculate = () => {
    const tax = calculateTax(income);
    setCalculatedTax(tax);
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <input
        type="number"
        className="border p-2 w-full rounded"
        value={income}
        onChange={(e) => setIncome(Number(e.target.value))}
        placeholder="Enter your annual income"
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleCalculate}
      >
        Calculate Tax
      </button>
      <div className="text-lg">
        Estimated Tax: <strong>£{calculatedTax}</strong>
      </div>
    </div>
  );
}