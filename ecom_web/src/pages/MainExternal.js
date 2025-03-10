import "bootstrap-icons/font/bootstrap-icons.css"; // Import Bootstrap Icons
import "bootstrap/dist/css/bootstrap.min.css";
import React, { useState } from "react";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function MainExternal() {
  const tiles = [
    { name: "Order Entry", bg: "primary", icon: "bi-box-arrow-in-right" },
    { name: "Order Tracking", bg: "success", icon: "bi-truck" },
    { name: "Purchase Order Upload", bg: "secondary", icon: "bi-gear" },
    { name: "Function 4", bg: "warning", icon: "bi-clipboard-data" },
    { name: "Function 5", bg: "danger", icon: "bi-exclamation-triangle" },
    { name: "Function 6", bg: "info", icon: "bi-bar-chart" },
    { name: "Function 7", bg: "dark", icon: "bi-graph-up" },
  ];

  const [hoveredIndex, setHoveredIndex] = useState(null);

  return (
    <div className="container mt-4">
      <div className="row g-3">
        {tiles.map((tile, index) => (
          <div key={index} className="col-md-4">
            <Link
              to={`/user-${tile.name.replace(/\s+/g, "-")}`}
              className="text-decoration-none"
            >
              <Card
                bg={tile.bg}
                text="white"
                className="shadow text-center"
                style={{
                  transform: hoveredIndex === index ? "scale(1.05)" : "scale(1)",
                  boxShadow:
                    hoveredIndex === index
                      ? "0px 10px 20px rgba(0, 0, 0, 0.3)"
                      : "0px 5px 10px rgba(0, 0, 0, 0.1)",
                  transition: "transform 0.3s ease, box-shadow 0.3s ease",
                  cursor: "pointer",
                }}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                <Card.Body>
                  <i className={`bi ${tile.icon} display-4 d-block mb-3`}></i> {/* Bootstrap Icon */}
                  <Card.Title className="fw-bold">{tile.name}</Card.Title>
                </Card.Body>
              </Card>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
