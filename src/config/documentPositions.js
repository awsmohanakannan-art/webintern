// Document Positioning Rules & Text Fitting Parameters (Canvas dimensions: 742 x 1054)

export const offerLetterPositions = {
  canvas: { width: 742, height: 1054 },
  title: { x: 50, y: 980, fontSize: 24, align: "left", color: "#0B3D91" },
  subtitle: { x: 50, y: 950, fontSize: 12, align: "left", color: "#2E7DFF" },
  issueDate: { x: 50, y: 900, fontSize: 11, align: "left", label: "Date: " },
  studentName: { x: 50, y: 880, fontSize: 11, maxWidth: 500, align: "left" },
  subject: { x: 50, y: 840, fontSize: 14, align: "left", color: "#082B66" },
  bodyStart: { x: 50, y: 800, width: 642, fontSize: 11, lineHeight: 16 },
  offerId: { x: 50, y: 550, fontSize: 10, align: "left" },
  signatureSection: { x: 50, y: 400, width: 642 }
};

export const certificatePositions = {
  canvas: { width: 742, height: 1054 },
  title: { x: 371, y: 960, fontSize: 30, align: "center", color: "#0B3D91" },
  subBadge: { x: 371, y: 920, fontSize: 14, align: "center", color: "#2E7DFF" },
  studentName: { x: 371, y: 820, fontSize: 26, maxWidth: 600, align: "center", color: "#082B66" },
  courseDescription: { x: 371, y: 760, width: 620, fontSize: 12, align: "center" },
  certificateId: { x: 371, y: 650, fontSize: 12, align: "center", color: "#0B3D91" },
  issueDate: { x: 100, y: 650, fontSize: 10, align: "left" },
  verificationStatus: { x: 642, y: 650, fontSize: 10, align: "right" }
};
