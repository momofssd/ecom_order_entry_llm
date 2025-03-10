import React, { useEffect, useState } from 'react';
import { Alert, Button, Card, Container, Form, Modal, Spinner, Table } from 'react-bootstrap';

const POuploadAdmin = () => {
  const [files, setFiles] = useState([]);
  const [customer, setCustomer] = useState('BA');
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [processedResults, setProcessedResults] = useState([]);
  const [error, setError] = useState(null);

  // States for PDF Modal
  const [modalShow, setModalShow] = useState(false);
  const [selectedPDFUrl, setSelectedPDFUrl] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState("");

  useEffect(() => {
    fetch('http://localhost:5000/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data))
      .catch(err => setError('Failed to load customers'));
  }, []);

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    const validFiles = selectedFiles.filter(file => file.type === 'application/pdf');

    if (validFiles.length !== selectedFiles.length) {
      setError('Some files were skipped. Only PDF files are allowed.');
    } else if (validFiles.length === 0) {
      setError('Please select valid PDF files');
    } else {
      setError(null);
    }

    setFiles(validFiles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setError('Please select at least one file');
      return;
    }
  
    setLoading(true);
    setError(null);
    setProcessedResults([]);
  
    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('customer', customer);
  
      try {
        const response = await fetch('http://localhost:5000/api/process-purchase-order', {
          method: 'POST',
          body: formData
        });
  
        if (!response.ok) {
          throw new Error(`Failed to process ${file.name}`);
        }
  
        const data = await response.json();
  
        // Process date and quantity formatting
        if (data['Required Delivery Date']) {
          const date = new Date(data['Required Delivery Date']);
          data['Required Delivery Date'] = date.toISOString().split('T')[0]; // YYYY-MM-DD
        }
        if (data['Quantity']) {
          data['Quantity'] = data['Quantity'].replace(/[^\d.]/g, ''); // Remove non-numeric characters
        }
        if (!data['Unit']) {
          data['Unit'] = "N/A"; // Fallback if Unit is missing
        }
  
        // Create a blob URL to view the PDF
        const fileURL = URL.createObjectURL(file);
  
        setProcessedResults(prevResults => [
          ...prevResults,
          {
            fileName: file.name,
            data: data,
            isEditing: false,
            fileUrl: fileURL
          }
        ]);
      } catch (error) {
        setError(error.message || 'Error processing purchase orders');
      }
    }
    setLoading(false);
  };

  const handleEditToggle = (index) => {
    setProcessedResults(prevResults =>
      prevResults.map((result, i) =>
        i === index ? { ...result, isEditing: !result.isEditing } : result
      )
    );
  };

  const handleDataChange = (index, key, value) => {
    setProcessedResults(prevResults =>
      prevResults.map((result, i) =>
        i === index ? {
          ...result,
          data: {
            ...result.data,
            [key]: value
          }
        } : result
      )
    );
  };

  const handleFinalSubmit = () => {
    console.log("Final Submitted Data:", processedResults);
  };

  // Handler to open the modal with the PDF viewer
  const handleViewPdf = (fileUrl, fileName) => {
    setSelectedPDFUrl(fileUrl);
    setSelectedFileName(fileName);
    setModalShow(true);
  };

  // New function to reset the page (reload the browser)
  const handleReset = () => {
    window.location.reload();
  };

  const fieldOrder = [
    "sold_to_num",
    "Deliver to",
    "Purchase Order Number",
    "Required Delivery Date",
    "Material Number",
    "Quantity",
    "Unit"
  ];

  const fieldMapping = {
    "sold_to_num": "Sold to",
    "Deliver to": "Deliver to",
    "Purchase Order Number": "Purchase Order Number",
    "Required Delivery Date": "Required Delivery Date",
    "Material Number": "Material Number",
    "Quantity": "Quantity",
    "Unit": "Unit of Measure"
  };

  return (
    <Container className="py-4">
      <Card className="mb-4">
        <Card.Header>
          <h4 className="mb-0">Purchase Order Processor</h4>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Select Customer</Form.Label>
              <Form.Select
                value={customer}
                onChange={(e) => setCustomer(e.target.value)}
              >
                {customers.map(({ value, label }) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Upload PDF Files</Form.Label>
              <Form.Control
                type="file"
                accept=".pdf"
                multiple
                onChange={handleFileChange}
              />
              <Form.Text className="text-muted">
                You can select multiple PDF files
              </Form.Text>
            </Form.Group>

            {error && (
              <Alert variant="danger" className="mb-3">
                {error}
              </Alert>
            )}

            <Button
              type="submit"
              variant="primary"
              disabled={loading || files.length === 0}
              className="w-100"
            >
              {loading ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    className="me-2"
                  />
                  Processing...
                </>
              ) : (
                'Process Purchase Orders'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {processedResults.length > 0 && (
        <Card className="mb-4">
          <Card.Header>
            <h5 className="mb-0">Processed Purchase Orders</h5>
          </Card.Header>
          <Card.Body>
            <Table responsive striped bordered>
              <thead>
                <tr>
                  <th>File Name</th>
                  {fieldOrder.map((key) => (
                    <th key={key}>{fieldMapping[key]}</th>
                  ))}
                  <th>View PDF</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {processedResults.map((result, index) => (
                  <tr key={index}>
                    <td>{result.fileName}</td>
                    {fieldOrder.map((key) => (
                      <td key={key}>
                        {result.isEditing ? (
                          <Form.Control
                            type="text"
                            value={result.data[key] || ""}
                            onChange={(e) => handleDataChange(index, key, e.target.value)}
                          />
                        ) : (
                          result.data[key] || "N/A"
                        )}
                      </td>
                    ))}
                    <td>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleViewPdf(result.fileUrl, result.fileName)}
                      >
                        View
                      </Button>
                    </td>
                    <td>
                      <Button
                        variant={result.isEditing ? "success" : "primary"}
                        size="sm"
                        onClick={() => handleEditToggle(index)}
                      >
                        {result.isEditing ? "Save" : "Edit"}
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
            <div className="d-flex justify-content-between mt-3">
              <Button
                variant="success"
                onClick={handleFinalSubmit}
              >
                Submit All
              </Button>
              <Button
                variant="warning"
                onClick={handleReset}
              >
                Reset
              </Button>
            </div>
          </Card.Body>
        </Card>
      )}

      {/* If no processed results, you can still reset the page */}
      {processedResults.length === 0 && (
        <Button variant="warning" onClick={handleReset} className="mt-3 w-100">
          Reset
        </Button>
      )}

      {/* Modal for viewing PDF */}
      <Modal
        show={modalShow}
        onHide={() => setModalShow(false)}
        size="lg"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{selectedFileName}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedPDFUrl && (
            <embed
             src={`${selectedPDFUrl}#view=FitH&zoom=90&toolbar=1&navpanes=0&scrollbar=1&pagemode=none`}
              type="application/pdf"
              width="100%"
              height="600px"
            />
          )}
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default POuploadAdmin;
