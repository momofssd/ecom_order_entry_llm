import React, { useEffect, useState } from "react";
import { Button, Container, Form, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as XLSX from "xlsx"; // Import XLSX for Excel file generation
import orders_data from "../../data/orders";

const OrderRecords = () => {
  const [data, setData] = useState(orders_data);
  const [filteredData, setFilteredData] = useState(orders_data);
  const [sortConfig, setSortConfig] = useState({ key: "", direction: "ascending" });
  const [filterItem, setFilterItem] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(8);

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);

  // Sorting logic
  const getDirection = (key) => {
    if (sortConfig.key !== key) {
      return "ascending";
    }
    return sortConfig.direction === "ascending" ? "descending" : "ascending";
  };

  const handleSort = (key) => {
    const direction = getDirection(key);
    const sortedData = [...filteredData].sort((a, b) => {
      if (a[key] < b[key]) return direction === "ascending" ? -1 : 1;
      if (a[key] > b[key]) return direction === "ascending" ? 1 : -1;
      return 0;
    });
    setSortConfig({ key, direction });
    setFilteredData(sortedData);
  };

  // Filter logic
  const applyFilter = (dataSet = []) => {
    return dataSet.filter((item) =>
      (item.order_number && item.order_number.toLowerCase().includes(filterItem.toLowerCase())) ||
      (item.status && item.status.toLowerCase().includes(filterItem.toLowerCase())) ||
      (item.payment_status && item.payment_status.toLowerCase().includes(filterItem.toLowerCase()))
    );
  };

  // Pagination logic
  const paginateData = () => {
    const startIdx = (currentPage - 1) * itemsPerPage;
    const endIdx = startIdx + itemsPerPage;
    return filteredData.slice(startIdx, endIdx);
  };

  const paginatedData = paginateData();

  useEffect(() => {
    const filtered = applyFilter(data);
    setFilteredData(filtered);
    setCurrentPage(1);
  }, [filterItem, data]);

  // 📌 Function to Download as Excel
  const downloadExcel = () => {
    const ws = XLSX.utils.json_to_sheet(data); // Convert JSON to worksheet
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Orders");
    XLSX.writeFile(wb, "Order_Records.xlsx"); // Generate and download file
  };

  return (
    <Container>
      <h2 className="text-center my-4">Order Records</h2>

      {/* Back to MainInternal Button & Download Excel Button */}
      <div className="d-flex justify-content-between mb-3">
        <Link to="/" className="btn btn-outline-secondary">⬅ Back to Main Page</Link>
        <Button variant="success" onClick={downloadExcel}>📥 Download Excel</Button>
      </div>

      <div className="d-flex justify-content-between align-items-center mb-3">
        {/* Search Input */}
        <Form.Control
          type="text"
          placeholder="Search orders..."
          value={filterItem}
          onChange={(e) => setFilterItem(e.target.value)}
          className="w-50"
        />

        {/* Items Per Page Selector */}
        <Form.Select
          className="w-25"
          value={itemsPerPage}
          onChange={(e) => {
            setItemsPerPage(Number(e.target.value));
            setCurrentPage(1);
          }}
        >
          <option value="5">Show 5 per page</option>
          <option value="8">Show 8 per page</option>
          <option value="10">Show 10 per page</option>
          <option value="20">Show 20 per page</option>
        </Form.Select>
      </div>

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            {Object.keys(orders_data[0]).map((key) => (
              <th key={key}>
                <Button
                  variant="link"
                  onClick={() => handleSort(key)}
                  className="p-0"
                >
                  {key.replace(/_/g, " ").toUpperCase()}{" "}
                  {sortConfig.key === key &&
                    (sortConfig.direction === "ascending" ? "↑" : "↓")}
                </Button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((item, idx) => (
            <tr key={idx}>
              {Object.keys(item).map((key) => (
                <td key={key}>{item[key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>

      <div className="d-flex justify-content-between align-items-center mt-3">
        <Button
          variant="outline-primary"
          onClick={() => setCurrentPage(Math.max(currentPage - 1, 1))}
          disabled={currentPage === 1}
        >
          Previous
        </Button>
        <span>
          Page {currentPage} / {totalPages}
        </span>
        <Button
          variant="outline-primary"
          onClick={() => setCurrentPage(Math.min(currentPage + 1, totalPages))}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </div>
    </Container>
  );
};

export default OrderRecords;
