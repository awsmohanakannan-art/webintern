// Resend Email Integration Service (Section 13)

export const emailService = {
  async sendPasswordResetEmail(email, resetLink) {
    const response = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, reset_link: resetLink })
    });
    return response.json();
  },

  async sendOfferLetterEmail(applicationId) {
    const response = await fetch(`/api/admin/documents/${applicationId}/resend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_type: 'OFFER_LETTER' })
    });
    return response.json();
  },

  async sendCertificateEmail(certificateId) {
    const response = await fetch(`/api/admin/documents/${certificateId}/resend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_type: 'CERTIFICATE' })
    });
    return response.json();
  }
};
