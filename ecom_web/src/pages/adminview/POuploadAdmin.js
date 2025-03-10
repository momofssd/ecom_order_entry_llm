import React, { useEffect, useRef, useState } from 'react';
import { Alert, Button, Card, Container, Form, Modal, Spinner, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const POuploadAdmin = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [files, setFiles] = useState([]);
  const [customer, setCustomer] = useState('');
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [processedResults, setProcessedResults] = useState([]);
  const [error, setError] = useState(null);
  const [shipToInfo, setShipToInfo] = useState({});

  // States for PDF Modal
  const [modalShow, setModalShow] = useState(false);
  const [selectedPDFUrl, setSelectedPDFUrl] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState("");

  useEffect(() => {
    fetch('http://localhost:5000/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        // Clear loaded PDF files when customers are loaded
        setFiles([]);
        setProcessedResults([]);
        // Reset file input
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      })
      .catch(err => setError('Failed to load customers'));
  }, []);

  // Fetch ship-to info when customer changes
  useEffect(() => {
    // Clear loaded PDF files when customer changes
    setFiles([]);
    setProcessedResults([]);
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    
    if (customer) {
      fetch(`http://localhost:5000/api/customer-ship-to/${customer}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch ship-to info');
          }
          return response.json();
        })
        .then(data => {
          setShipToInfo(data);
        })
        .catch(err => {
          console.error('Failed to load ship-to info:', err);
          setShipToInfo({});
        });
    } else {
      // Clear ship-to info when no customer is selected
      setShipToInfo({});
    }
  }, [customer]);

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
        let data;
        
        // ===== DEFAULT CUSTOMER HANDLING =====
        // When DEFAULT is selected, we use standard_via_openai.py directly via a special endpoint
        // This bypasses the regular processing flow (utils.py, po_process.py, llm_process.py)
        if (customer.toUpperCase() === 'DEFAULT') {
          // Create a special endpoint for DEFAULT customer that uses standard_via_openai directly
          const response = await fetch('http://localhost:5000/api/process-default-purchase-order', {
            method: 'POST',
            body: formData
          });
          
          if (!response.ok) {
            throw new Error(`Failed to process ${file.name}`);
          }
          
          // Get the array of line items from standard_via_openai.py's extract_po_data function
          // This is where we receive and use the output from standard_via_openai.py
          const lineItems = await response.json();
          
          // Handle multiple line items from standard_via_openai
          if (lineItems && lineItems.length > 0) {
            // Create a blob URL to view the PDF
            const fileURL = URL.createObjectURL(file);
            
            // Process each line item and add it to the results
            lineItems.forEach((line, index) => {
              // Map the fields from standard_via_openai format to the expected format
              const processedData = {
                'Purchase Order Number': line['Purchase Order Number'] || '',
                'Required Delivery Date': line['Required Delivery Date'] || '',
                'Material Number': line['Material Number'] || '',
                'Quantity': line['Order Quantity in kg'] ? line['Order Quantity in kg'].toString() : '0',
                'Deliver to': line['Delivery Address'] || '',
                'Unit': 'kg', // Default unit for standard_via_openai is kg
                'sold_to_num': line['Customer Name'] || 'DEFAULT' // Use extracted Customer Name instead of hardcoding DEFAULT
              };
              
              // Process date formatting
              if (processedData['Required Delivery Date']) {
                const date = new Date(processedData['Required Delivery Date']);
                if (!isNaN(date.getTime())) { // Check if date is valid
                  processedData['Required Delivery Date'] = date.toISOString().split('T')[0]; // YYYY-MM-DD
                }
              }
              
              // Add line item to processed results
              setProcessedResults(prevResults => [
                ...prevResults,
                {
                  fileName: index === 0 ? file.name : `${file.name} (Line ${index + 1})`,
                  data: processedData,
                  isEditing: false,
                  fileUrl: fileURL
                }
              ]);
            });
            
            // Skip the rest of the loop since we've already added all line items
            continue;
          } else {
            throw new Error(`No data extracted from ${file.name}`);
          }
        } else {
          // For other customers, use the regular process-purchase-order endpoint
          const response = await fetch('http://localhost:5000/api/process-purchase-order', {
            method: 'POST',
            body: formData
          });
          
          if (!response.ok) {
            throw new Error(`Failed to process ${file.name}`);
          }
          
          data = await response.json();
        }
  
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

  // Handler to open the PDF in a new browser window
  const handleViewPdf = (fileUrl, fileName) => {
    // Try to open in a new window first
    const newWindow = window.open(
      `${fileUrl}#view=Fit&zoom=100&toolbar=1&navpanes=1&scrollbar=1&pagemode=none`, 
      '_blank'
    );
    
    // If popup is blocked or fails, fallback to modal
    if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
      // Fallback to modal if popup is blocked
      setSelectedPDFUrl(fileUrl);
      setSelectedFileName(fileName);
      setModalShow(true);
    }
  };

  // New function to reset the page (reload the browser)
  const handleReset = () => {
    window.location.reload();
  };

  // Field order with all important columns including Deliver to
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
    "sold_to_num": "Customer",
    "Deliver to": "Ship To",
    "Purchase Order Number": "PO Number",
    "Required Delivery Date": "Delivery Date",
    "Material Number": "Material #",
    "Quantity": "Qty",
    "Unit": "UoM"
  };

  // Handler to navigate back to the admin dashboard
  const handleBack = () => {
    navigate('/admin/dashboard');
  };

  return (
    <Container fluid className="py-4 px-2" style={{ maxWidth: '100%' }}>
      <Button 
        variant="outline-secondary" 
        className="mb-3" 
        onClick={handleBack}
      >
        <i className="bi bi-arrow-left"></i> Back to Dashboard
      </Button>
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
                <option value="">Select a customer...</option>
                {customers.map(({ value, label }) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </Form.Select>
            </Form.Group>

            {/* Ship-to Information Display */}
            {Object.keys(shipToInfo).length > 0 && (
              <Card className="mb-3">
                <Card.Header>
                  <h5 className="mb-0">Ship-to Information</h5>
                </Card.Header>
                <Card.Body>
                  <Table striped bordered size="sm" style={{ fontSize: '0.85rem' }}>
                    <thead>
                      <tr>
                        <th>Ship-to Code</th>
                        <th>Address</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(shipToInfo).map(([key, value]) => (
                        <tr key={key}>
                          <td><strong>{key}</strong></td>
                          <td>{value}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            )}

            <Form.Group className="mb-3">
              <Form.Label>Upload PDF Files</Form.Label>
              <Form.Control
                ref={fileInputRef}
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
            <Table striped bordered size="sm" style={{ fontSize: '1rem' }}>
              <thead>
                <tr>
                  <th style={{ width: '120px' }}>File Name</th>
                  {fieldOrder.map((key, index) => (
                    <th key={key} style={key === "Deliver to" ? { width: '150px' } : {}}>
                      {fieldMapping[key]}
                    </th>
                  ))}
                  <th style={{ width: '80px' }}>View PDF</th>
                  <th style={{ width: '80px' }}>Actions</th>
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
              src={`${selectedPDFUrl}#view=Fit&zoom=100&toolbar=1&navpanes=1&scrollbar=1&pagemode=none`}
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
