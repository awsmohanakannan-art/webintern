// Certificate Automation Job Service (Section 27)

export async function runCertificateIssuanceJob() {
  try {
    const response = await fetch('/api/admin/certificates/run-issuance-job', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
  } catch (error) {
    console.error('[Certificate Job Exception]:', error);
    return { error: error.message };
  }
}
