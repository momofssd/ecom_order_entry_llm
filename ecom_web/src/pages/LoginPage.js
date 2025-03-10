import "bootstrap/dist/css/bootstrap.min.css";
import React, { useEffect, useState } from "react";
import { Alert, Button, Col, Form, Row } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { users } from "../users"; // Import users

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  // ✅ Redirect if already logged in using sessionStorage
  useEffect(() => {
    const loggedInUser = JSON.parse(sessionStorage.getItem("loggedInUser"));
    if (loggedInUser) {
      const redirectPath = loggedInUser.isAdmin ? "/MainInternal" : "/MainExternal";
      navigate(redirectPath);
    }
  }, [navigate]);

  const handleSubmit = (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!username || !password) {
      setError("Username and password are required.");
      return;
    }

    // ✅ Use imported `users` to validate login
    const userObject = users.find((user) => user.username === username && user.password === password);

    if (userObject) {
      // Store user in sessionStorage instead of localStorage
      sessionStorage.setItem("loggedInUser", JSON.stringify(userObject));
      setSuccess("Login successful! Redirecting...");

      const redirectPath = userObject.isAdmin ? "/MainInternal" : "/MainExternal";
      setTimeout(() => navigate(redirectPath), 1000);
    } else {
      setError("Invalid username or password.");
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="w-25">
        <h2 className="text-center mb-4">Login</h2>

        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>

          <Button type="submit" className="w-100" style={{ backgroundColor: "#1177b8" }}>
            Login
          </Button>
        </Form>

        <Row className="mt-3">
          <Col className="text-center">Don't have an account? Register</Col>
        </Row>
      </div>
    </div>
  );
};

export default LoginPage;
