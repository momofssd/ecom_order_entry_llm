import React, { useState } from "react";
import { Button, Container, Form, Modal, Table } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function OrderEntry() {
  const emptyRow = { 
    soldTo: "", 
    shipTo: "", 
    purchaseOrder: "", 
    deliveryDate: "", 
    partNumber: "", 
    qty: "", 
    uom: "" 
  };

  const [orders, setOrders] = useState([emptyRow]); // Default: 1 empty row
  const [showModal, setShowModal] = useState(false); // Controls modal visibility

  // Function to handle input changes
  const handleInputChange = (index, field, value) => {
    const updatedOrders = [...orders];
    updatedOrders[index][field] = value;
    setOrders(updatedOrders);
  };

  // Function to add a new row
  const addRow = () => {
    setOrders([...orders, emptyRow]);
  };

  // Function to submit all rows (triggers modal)
  const submitOrders = () => {
    console.log("Submitted Orders:", orders);
    setShowModal(true); // Show Bootstrap modal
  };

  // Function to clear all rows (reset to 1 empty row)
  const clearAll = () => {
    setOrders([emptyRow]); // Resets to a single empty row
  };

  return (
    <Container>
      <h2 className="text-center my-4">Order Entry</h2>
      <div className="d-flex justify-content-between mb-3">
        <Link to="/" className="btn btn-outline-secondary">⬅ Back to Main Page</Link>
      </div>
      <Table bordered hover responsive>
        <thead>
          <tr>
            <th>Sold-to Number</th>
            <th>Ship-to Number</th>
            <th>Purchase Order</th>
            <th>Required Delivery Date (ISO Format)</th>
            <th>Part Number</th>
            <th>Quantity</th>
            <th>Unit of Measure</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order, index) => (
            <tr key={index}>
              <td>
                <Form.Control
                  type="text"
                  value={order.soldTo}
                  onChange={(e) => handleInputChange(index, "soldTo", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="text"
                  value={order.shipTo}
                  onChange={(e) => handleInputChange(index, "shipTo", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="text"
                  value={order.purchaseOrder}
                  onChange={(e) => handleInputChange(index, "purchaseOrder", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="date"
                  value={order.deliveryDate}
                  onChange={(e) => handleInputChange(index, "deliveryDate", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="text"
                  value={order.partNumber}
                  onChange={(e) => handleInputChange(index, "partNumber", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="number"
                  value={order.qty}
                  onChange={(e) => handleInputChange(index, "qty", e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="text"
                  value={order.uom}
                  onChange={(e) => handleInputChange(index, "uom", e.target.value)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Buttons */}
      <div className="d-flex justify-content-between mt-3">
        <Button variant="primary" onClick={addRow}>
          ➕ Add Row
        </Button>
        <Button variant="danger" onClick={clearAll}>
          🗑 Clear All
        </Button>
        <Button variant="success" onClick={submitOrders}>
          ✅ Submit Orders
        </Button>
      </div>

      {/* Bootstrap Modal for Order Submission */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Order Submitted</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Your order has been successfully submitted! 🎉 <br />
          Check the console for submitted data.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
