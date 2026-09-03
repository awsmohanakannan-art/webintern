// Administrator Portal View (Section 40 Requirements)
const AdminView = {
  async render() {
    const user = API.getCurrentUser();
    const container = document.getElementById('app-view');
    if (!container) return;

    if (!user || user.role !== 'admin') {
      this.renderAdminLogin();
      return;
    }

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <!-- Back Navigation Bar (Section 12 Navigation Fix) -->
          <div style="margin-bottom: 20px;">
            <a href="#/" class="btn btn-outline btn-sm" style="display: inline-flex; align-items: center; gap: 6px;">
              <i data-feather="arrow-left" style="width:14px; height:14px;"></i> ← Return to Main Site
            </a>
          </div>

          <!-- Header Bar -->
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px; border: 1px solid var(--color-border); margin-bottom: 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
            <div>
              <span class="badge-sector" style="background:#082B66; color:#fff;">ADMINISTRATION PORTAL</span>
              <h1 style="font-size: 30px; color: var(--color-blue-dark); margin-top: 6px;">Platform Management & Automation Panel</h1>
              <p style="color: var(--color-gray-text); font-size: 14px;">Grade PDF deliverables, trigger automated certificates, resend document emails, and sync Google Sheets records.</p>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button onclick="AdminView.runCertificateJob()" class="btn btn-primary btn-sm">
                ⚡ Run Certificate Job
              </button>
              <button onclick="AdminView.retrySheetsSync()" class="btn btn-outline btn-sm">
                📊 Retry Sheets Sync
              </button>
              <button onclick="HeaderComponent.logout()" class="btn btn-outline btn-sm">Admin Sign Out</button>
            </div>
          </div>

          <!-- Stats Overview -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 36px;" id="admin-stats-counters">
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">TOTAL STUDENTS</span>
              <h2 style="font-size: 32px; color: var(--color-primary-blue);" id="stat-students">-</h2>
            </div>
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">APPLICATIONS</span>
              <h2 style="font-size: 32px; color: var(--color-primary-blue);" id="stat-apps">-</h2>
            </div>
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">PENDING REVIEWS</span>
              <h2 style="font-size: 32px; color: #F59E0B;" id="stat-pending">-</h2>
            </div>
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">CERTIFICATES ISSUED</span>
              <h2 style="font-size: 32px; color: #10B981;" id="stat-certs">-</h2>
            </div>
          </div>

          <!-- Pending Task Deliverable Submissions (Section 23 Admin Grading) -->
          <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 32px; margin-bottom: 32px;">
            <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 20px;">Assignment Deliverables Review & Grading</h2>
            <div id="admin-submissions-list">Loading submissions...</div>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();
    await this.loadAdminData();
  },

  renderAdminLogin() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg); min-height: calc(100vh - 72px); display: flex; align-items: center; justify-content: center;">
        <div class="container" style="max-width: 420px;">
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 40px 32px; border: 1px solid var(--color-border); box-shadow: var(--shadow-xl);">
            
            <div style="text-align: center; margin-bottom: 28px;">
              <div style="width: 48px; height: 48px; border-radius: 50%; background: var(--color-blue-dark); color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto;">
                <i data-feather="shield" style="width: 24px; height: 24px;"></i>
              </div>
              <h1 style="font-size: 24px; color: var(--color-blue-dark); margin-bottom: 6px;">Administrator Sign In</h1>
              <p style="color: var(--color-gray-text); font-size: 13px;">Default admin: admin@webintern.com / admin123</p>
            </div>

            <form id="admin-login-form">
              <div class="form-group">
                <label class="form-label">Admin Email</label>
                <input type="email" id="admin-email" class="form-input" value="admin@webintern.com" required />
              </div>

              <div class="form-group">
                <label class="form-label">Password</label>
                <input type="password" id="admin-password" class="form-input" value="admin123" required />
              </div>

              <button type="submit" class="btn btn-primary btn-full btn-lg">
                Sign In to Admin Panel
              </button>
            </form>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    document.getElementById('admin-login-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('admin-email').value.trim();
      const password = document.getElementById('admin-password').value.trim();

      try {
        Toast.show('Authenticating administrator credentials...', 'info');
        const res = await API.request('/api/auth/admin/login', {
          method: 'POST',
          body: { email, password }
        });

        API.setAuthToken(res.token);
        API.setCurrentUser(res.user);
        HeaderComponent.updateAuthState();
        Toast.show('Admin login successful!', 'success');
        this.render();
      } catch (err) {
        Toast.show(err.message || 'Invalid administrator password.', 'error');
      }
    });
  },

  async loadAdminData() {
    try {
      const statsRes = await API.request('/api/admin/stats');
      if (statsRes.stats) {
        document.getElementById('stat-students').innerText = statsRes.stats.total_students;
        document.getElementById('stat-apps').innerText = statsRes.stats.total_applications;
        document.getElementById('stat-pending').innerText = statsRes.stats.pending_reviews;
        document.getElementById('stat-certs').innerText = statsRes.stats.issued_certificates;
      }

      const subsRes = await API.request('/api/admin/submissions');
      const listContainer = document.getElementById('admin-submissions-list');
      if (!listContainer) return;

      if (!subsRes.submissions || subsRes.submissions.length === 0) {
        listContainer.innerHTML = `<p style="color: var(--color-gray-text);">No pending submissions to review.</p>`;
        return;
      }

      listContainer.innerHTML = subsRes.submissions.map(s => `
        <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 16px; background: var(--color-gray-bg);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
            <div>
              <strong style="font-size: 16px; color: var(--color-blue-dark);">${s.student_name}</strong> (${s.student_email})
              <div style="font-size: 13px; color: var(--color-gray-text); margin-top: 2px;">
                <strong>${s.internship_title}</strong> — Week ${s.week_number}: ${s.task_title || 'Module Deliverable'}
              </div>
            </div>
            <span style="font-size: 11px; font-weight: 700; color: white; background: ${['approved','graded'].includes(s.status) ? '#10B981' : (s.status === 'pending' ? '#3B82F6' : '#EF4444')}; padding: 4px 12px; border-radius: 99px; text-transform: uppercase;">
              ${s.status}
            </span>
          </div>

          <div style="margin-bottom: 14px;">
            <a href="${s.file_url}" target="_blank" class="btn btn-outline btn-sm" style="background: white;">
              <i data-feather="external-link" style="width: 14px;"></i> View / Download Submitted PDF
            </a>
          </div>

          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input type="number" id="marks-input-${s.id}" min="0" max="10" class="form-input" placeholder="Marks (0-10)" value="${s.marks !== null && s.marks !== undefined ? s.marks : 8}" style="width: 110px; font-size: 13px; padding: 8px 12px;" />
            <input type="text" id="feedback-input-${s.id}" class="form-input" placeholder="Feedback for student..." value="${s.feedback || 'Great work! Deliverable approved.'}" style="flex: 1; font-size: 13px; padding: 8px 12px;" />
            <button onclick="AdminView.grade('${s.id}', 'graded')" class="btn btn-primary btn-sm" style="background: #10B981; border-color: #10B981; white-space: nowrap;">
              Grade & Approve
            </button>
            <button onclick="AdminView.grade('${s.id}', 'revise')" class="btn btn-outline btn-sm" style="color: #EF4444; border-color: #EF4444; white-space: nowrap;">
              Request Revision
            </button>
          </div>
        </div>
      `).join('');

      if (window.feather) feather.replace();
    } catch (e) {
      console.error("Load admin data error:", e);
    }
  },

  async grade(subId, status) {
    const marks = parseFloat(document.getElementById(`marks-input-${subId}`)?.value || 8);
    const feedback = document.getElementById(`feedback-input-${subId}`)?.value.trim();

    try {
      Toast.show(`Grading submission...`, 'info');
      const res = await API.request(`/api/admin/submissions/${subId}/grade`, {
        method: 'POST',
        body: { status, marks, max_marks: 10, feedback }
      });
      Toast.show(res.message || 'Submission graded!', 'success');
      this.loadAdminData();
    } catch (e) {
      Toast.show(e.message || 'Grading action failed.', 'error');
    }
  },

  async runCertificateJob() {
    try {
      Toast.show('Executing Certificate Automation Job...', 'info');
      const res = await API.request('/api/admin/certificates/run-issuance-job', { method: 'POST' });
      Toast.show(res.message, 'success');
      this.loadAdminData();
    } catch (e) {
      Toast.show(e.message || 'Certificate job execution failed.', 'error');
    }
  },

  async retrySheetsSync() {
    try {
      Toast.show('Triggering Google Sheets Sync Retry...', 'info');
      const res = await API.request('/api/admin/sheets/retry', { method: 'POST' });
      Toast.show(res.message, 'success');
    } catch (e) {
      Toast.show(e.message || 'Google Sheets sync retry failed.', 'error');
    }
  }
};
