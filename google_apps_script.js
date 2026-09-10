/**
 * WebIntern Google Apps Script Webhook Endpoint for Google Sheets Tracking
 * Paste this into Google Apps Script connected to your Google Spreadsheet.
 * Deploy as Web App -> Execute as: Me -> Who has access: Anyone.
 */

function doPost(e) {
  try {
    var contents = {};
    if (e && e.postData && e.postData.contents) {
      try {
        contents = JSON.parse(e.postData.contents);
      } catch (pErr) {
        contents = e.parameter || {};
      }
    } else if (e && e.parameter) {
      if (e.parameter.payload) {
        try {
          contents = JSON.parse(e.parameter.payload);
        } catch(pErr2) {
          contents = e.parameter;
        }
      } else {
        contents = e.parameter;
      }
    }

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var docType = contents.type || contents.documentType;

    if (docType === "USER_REGISTRATION" || docType === "USER_LOGIN") {
      var sheet = ss.getSheetByName("Student Logins & Signups") || ss.insertSheet("Student Logins & Signups");
      if (sheet.getLastRow() === 0) {
        sheet.appendRow([
          "Timestamp", "Event Type", "Student ID", "Student Name", "Student Email", 
          "Mobile", "College Name", "Department", "Degree", "Auth Provider"
        ]);
      }
      sheet.appendRow([
        contents.timestamp || new Date().toISOString(),
        docType,
        contents.studentId || contents.student_id || "",
        contents.studentName || contents.student_name || "",
        contents.email || contents.student_email || "",
        contents.mobile || contents.phone || contents.student_mobile || "",
        contents.collegeName || contents.college || "",
        contents.department || "",
        contents.degree || "",
        contents.authProvider || "email"
      ]);
    } else if (docType === "OFFER_LETTER") {
      var sheet = ss.getSheetByName("Offer Letters") || ss.insertSheet("Offer Letters");
      if (sheet.getLastRow() === 0) {
        sheet.appendRow([
          "Timestamp", "Offer ID", "Student ID", "Student Name", "Student Email", 
          "Mobile", "College Name", "Department", "Degree", "Course/Internship", "Internship Role", 
          "Company", "Start Date", "End Date", "Duration", "Location", "Mentor Name", 
          "Issue Date", "Document Status", "Email Status", "Email Message ID"
        ]);
      }
      sheet.appendRow([
        new Date().toISOString(),
        contents.offerId || contents.offer_id || "",
        contents.studentId || contents.student_id || "",
        contents.studentName || contents.student_name || "",
        contents.email || contents.student_email || "",
        contents.mobile || contents.phone || contents.student_mobile || "",
        contents.collegeName || contents.college || "",
        contents.department || "",
        contents.degree || "",
        contents.course || contents.course_name || "",
        contents.internshipRole || contents.role || "",
        contents.company || "Web Intern Platform",
        contents.startDate || contents.start_date || "",
        contents.endDate || contents.end_date || "",
        contents.duration || "4 Weeks",
        contents.location || "Virtual / Remote",
        contents.mentorName || contents.guideName || contents.mentor || "",
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
          "Mobile", "College Name", "Department", "Degree", "Course/Internship", "Internship Role", 
          "Company", "Start Date", "End Date", "Duration", "Guide Name", "Project Name", 
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
        contents.mobile || contents.phone || contents.student_mobile || "",
        contents.collegeName || contents.college || "",
        contents.department || "",
        contents.degree || "",
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

function doGet(e) {
  try {
    if (e) {
      return doPost(e);
    }
    return ContentService.createTextOutput(JSON.stringify({ 
      status: "online", 
      message: "WebIntern Google Sheets Webhook is active and tracking all fields including Mobile Phone Numbers!" 
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
