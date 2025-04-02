import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    basic_salary: "",
    incentives: "",
    spends: "",
    recharge: "",
    grocery: ""
  });

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    // Handle empty values gracefully
    const value = e.target.value === "" ? "" : parseFloat(e.target.value);
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Validate all fields are numbers
      const hasEmptyValues = Object.values(formData).some(val => val === "");
      if (hasEmptyValues) {
        throw new Error("Please fill all fields with valid numbers");
      }

      // Convert all values to numbers
      const payload = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, Number(value)])
      );

      const response = await axios.post(
        process.env.REACT_APP_API_URL || "https://salary-management-backend.onrender.com/api/calculate",
        payload,
        {
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          }
        }
      );

      if (!response.data || !response.data.calculations) {
        throw new Error("Invalid response format from server");
      }

      setReport(response.data);
    } catch (error) {
      console.error("Error details:", error);
      setError(error.message || "Failed to calculate salary");
    } finally {
      setLoading(false);
    }
  };

  const chartData = report 
    ? {
        labels: ["Income", "Expenses", "Savings"],
        datasets: [
          {
            label: "Amount ($)",
            data: [
              report.calculations.total_income,
              report.calculations.total_expenses,
              report.calculations.net_savings
            ],
            backgroundColor: [
              "rgba(75, 192, 192, 0.6)",
              "rgba(255, 99, 132, 0.6)",
              "rgba(54, 162, 235, 0.6)"
            ],
            borderColor: [
              "rgba(75, 192, 192, 1)",
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)"
            ],
            borderWidth: 1
          }
        ]
      } 
    : null;


  return (
    <div className="container">
      <h1>Employee Salary Management</h1>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Basic Salary ($)</label>
          <input
            type="number"
            name="basic_salary"
            value={formData.basic_salary}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Incentives ($)</label>
          <input
            type="number"
            name="incentives"
            value={formData.incentives}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Spends ($)</label>
          <input
            type="number"
            name="spends"
            value={formData.spends}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Recharge ($)</label>
          <input
            type="number"
            name="recharge"
            value={formData.recharge}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Grocery ($)</label>
          <input
            type="number"
            name="grocery"
            value={formData.grocery}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Calculating..." : "Calculate"}
        </button>
      </form>

      {report && (
        <div className="report">
          <h2>Salary Report</h2>

          <div className="chart-container">
            <Bar data={chartData} />
          </div>

          <div className="calculations">
            <p>
              <strong>Total Income:</strong> $
              {report.calculations.total_income.toFixed(2)}
            </p>
            <p>
              <strong>Total Expenses:</strong> $
              {report.calculations.total_expenses.toFixed(2)}
            </p>
            <p>
              <strong>Net Savings:</strong> $
              {report.calculations.net_savings.toFixed(2)}
            </p>
            <p>
              <strong>Savings Percentage:</strong>{" "}
              {report.calculations.savings_percentage.toFixed(2)}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
