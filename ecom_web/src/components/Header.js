import React, { useEffect, useState } from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";

const Header = () => {
  const [loggedInUser, setLoggedInUser] = useState(null);
  const location = useLocation();

  // Load logged-in user from sessionStorage on mount and when location changes
  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem("loggedInUser"));
    setLoggedInUser(user);
  }, [location]);

  const handleSignOut = () => {
    sessionStorage.removeItem("loggedInUser");
    setLoggedInUser(null); // Update state to force re-render
    window.location.href = "/"; // Redirect to the login page (or home)
  };

  return (
    <header>
      <Navbar style={{ backgroundColor: "#1177b8" }} variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <Navbar.Brand as={Link} to="/">ECart</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {/* Admin Panel (Only for Admins) */}
              {loggedInUser?.isAdmin && (
                <Nav.Link as={Link} to="/admin">
                  <i className="bi bi-shield-lock"> Admin Panel</i>
                </Nav.Link>
              )}

              {/* Profile (Visible for All Logged-in Users) */}
              {loggedInUser && (
                <Nav.Link as={Link} to="/profile">
                  <i className="bi bi-person-badge"> Profile</i>
                </Nav.Link>
              )}

              {/* Sign Out (Visible for All Logged-in Users) */}
              {loggedInUser && (
                <Nav.Link onClick={handleSignOut} style={{ cursor: "pointer" }}>
                  <i className="bi bi-box-arrow-right"> Sign Out</i>
                </Nav.Link>
              )}

              {/* Log In (Visible for Non-Logged-in Users) */}
              {!loggedInUser && (
                <Nav.Link as={Link} to="/login">
                  <i className="bi bi-box-arrow-in-right"> Log In</i>
                </Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
