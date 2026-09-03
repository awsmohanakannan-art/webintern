/**
 * WebIntern Google Apps Script Webhook Endpoint for Google Sheets Tracking
 * Paste this into Google Apps Script connected to your Google Spreadsheet.
 * Deploy as Web App -> Execute as: Me -> Who has access: Anyone.
 */

function doPost(e) {
  try {
    var contents = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var docType = contents.type || contents.documentType;

    if (docType === "OFFER_LETTER") {
      var sheet = ss.getSheetByName("Offer Letters") || ss.insertSheet("Offer Letters");
      if (sheet.getLastRow() === 0) {
        sheet.appendRow([
          "Timestamp", "Offer ID", "Student ID", "Student Name", "Student Email", 
          "Mobile", "College Name", "Course/Internship", "Internship Role", 
          "Company", "Start Date", "End Date", "Duration", "Location", 
          "Issue Date", "Document Status", "Email Status", "Email Message ID"
        ]);
      }
      sheet.appendRow([
        new Date().toISOString(),
        contents.offerId || contents.offer_id || "",
        contents.studentId || contents.student_id || "",
        contents.studentName || contents.student_name || "",
        contents.email || contents.student_email || "",
        contents.mobile || "",
        contents.collegeName || contents.college || "",
        contents.course || contents.course_name || "",
        contents.internshipRole || contents.role || "",
        contents.company || "Web Intern Platform",
        contents.startDate || contents.start_date || "",
        contents.endDate || contents.end_date || "",
        contents.duration || "4 Weeks",
        contents.location || "Virtual / Remote",
        contents.issueDate || contents.issue_date || "",
        contents.documentStatus || "ISSUED",
        contents.emailStatus || "SENT",
        contents.emailMessageId || ""
      ]);
    } else if (docType === "CERTIFICATE") {
      var sheet = ss.getSheetByName("Certificates") || ss.insertSheet("Certificates");
      if (sheet.getLastRow() === 0) {
        sheet.appendRow([
          "Timestamp", "Certificate ID", "Student ID", "Student Name", "Student Email", 
          "College Name", "Course/Internship", "Internship Role", "Company", 
          "Start Date", "End Date", "Duration", "Guide Name", "Project Name", 
          "Certificate Date", "Issue Date", "Document Status", "Email Status", 
          "Email Message ID", "Verification URL"
        ]);
      }
      sheet.appendRow([
        new Date().toISOString(),
        contents.certificateId || contents.certificate_id || "",
        contents.studentId || contents.student_id || "",
        contents.studentName || contents.student_name || "",
        contents.email || contents.student_email || "",
        contents.collegeName || contents.college || "",
        contents.course || contents.course_name || "",
        contents.internshipRole || contents.role || "",
        contents.company || "Web Intern Platform",
        contents.startDate || contents.start_date || "",
        contents.endDate || contents.end_date || "",
        contents.duration || "4 Weeks",
        contents.guideName || contents.guide || "",
        contents.projectName || contents.project || "",
        contents.certificateDate || contents.issue_date || "",
        contents.issueDate || contents.issue_date || "",
        contents.documentStatus || "ISSUED",
        contents.emailStatus || "SENT",
        contents.emailMessageId || "",
        contents.verificationUrl || ""
      ]);
    }

    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
