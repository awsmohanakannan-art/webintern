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
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px; border: 1px solid var(--color-border); margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
            <div>
              <span class="badge-sector" style="background:#082B66; color:#fff;">ADMINISTRATION PORTAL</span>
              <h1 style="font-size: 30px; color: var(--color-blue-dark); margin-top: 6px;">Master Internship & Document Management</h1>
              <p style="color: var(--color-gray-text); font-size: 14px; margin-top: 4px;">Unified single source-of-truth master records, automated PDF offer letters & certificates, and deliverable grading.</p>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button onclick="AdminView.openMasterFormModal()" class="btn btn-primary btn-sm">
                + Create Master Internship Record
              </button>
              <button onclick="AdminView.runCertificateJob()" class="btn btn-outline btn-sm">
                ⚡ Run Certificate Job
              </button>
              <button onclick="AdminView.retrySheetsSync()" class="btn btn-outline btn-sm">
                📊 Retry Sheets Sync
              </button>
              <button onclick="HeaderComponent.logout()" class="btn btn-outline btn-sm">Admin Sign Out</button>
            </div>
          </div>

          <!-- Tab Navigation Bar -->
          <div style="display: flex; gap: 12px; margin-bottom: 24px; border-bottom: 2px solid var(--color-border); padding-bottom: 12px;">
            <button onclick="AdminView.switchTab('master')" id="admin-tab-btn-master" class="btn btn-primary btn-sm">
              📋 Master Internship Records
            </button>
            <button onclick="AdminView.switchTab('submissions')" id="admin-tab-btn-submissions" class="btn btn-outline btn-sm">
              📥 Student Deliverables
            </button>
            <button onclick="AdminView.switchTab('settings')" id="admin-tab-btn-settings" class="btn btn-outline btn-sm">
              ⚙️ Organization Settings
            </button>
          </div>

          <!-- Stats Overview -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 28px;" id="admin-stats-counters">
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">TOTAL STUDENTS</span>
              <h2 style="font-size: 32px; color: var(--color-primary-blue);" id="stat-students">-</h2>
            </div>
            <div style="background: white; border-radius: var(--radius-md); padding: 20px; border: 1px solid var(--color-border); text-align: center;">
              <span style="font-size: 12px; font-weight:700; color: var(--color-gray-text);">MASTER RECORDS</span>
              <h2 style="font-size: 32px; color: var(--color-primary-blue);" id="stat-master-recs">-</h2>
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

          <!-- TAB 1: Master Internship Records Management -->
          <div id="admin-tab-content-master">
            <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 28px; margin-bottom: 32px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
                <div>
                  <h2 style="font-size: 22px; color: var(--color-blue-dark); margin: 0;">Single Source-of-Truth Master Records</h2>
                  <p style="font-size: 13px; color: var(--color-gray-text); margin-top: 4px;">Student information is stored ONCE and automatically populates into Offer Letters and Certificates.</p>
                </div>
                <button onclick="AdminView.openMasterFormModal()" class="btn btn-primary btn-sm">
                  + Add New Master Record
                </button>
              </div>

              <div id="master-records-table-container">
                <div style="text-align: center; padding: 40px; color: var(--color-gray-text);">Loading Master Internship Records...</div>
              </div>
            </div>
          </div>

          <!-- TAB 2: Submissions Review -->
          <div id="admin-tab-content-submissions" style="display: none;">
            <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 28px; margin-bottom: 32px;">
              <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 20px;">Assignment Deliverables Review & Grading</h2>
              <div id="admin-submissions-list">Loading submissions...</div>
            </div>
          </div>

          <!-- TAB 3: Organization Settings -->
          <div id="admin-tab-content-settings" style="display: none;">
            <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 32px; margin-bottom: 32px; max-width: 720px;">
              <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 6px;">Global Organization Settings</h2>
              <p style="font-size: 13px; color: var(--color-gray-text); margin-bottom: 24px;">Global values used automatically for all generated document headers, signatures, and credentials.</p>

              <form onsubmit="AdminView.saveOrgSettings(event)">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                  <div>
                    <label class="form-label">Organization Name *</label>
                    <input type="text" id="org-name" class="form-input" required />
                  </div>
                  <div>
                    <label class="form-label">Website *</label>
                    <input type="text" id="org-website" class="form-input" required />
                  </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                  <div>
                    <label class="form-label">Organization Email *</label>
                    <input type="email" id="org-email" class="form-input" required />
                  </div>
                  <div>
                    <label class="form-label">Location / Address</label>
                    <input type="text" id="org-address" class="form-input" />
                  </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                  <div>
                    <label class="form-label">Founder Name *</label>
                    <input type="text" id="org-founder-name" class="form-input" required />
                  </div>
                  <div>
                    <label class="form-label">Founder Designation *</label>
                    <input type="text" id="org-founder-desig" class="form-input" required />
                  </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                  <div>
                    <label class="form-label">Technical Director Name *</label>
                    <input type="text" id="org-td-name" class="form-input" required />
                  </div>
                  <div>
                    <label class="form-label">Technical Director Designation *</label>
                    <input type="text" id="org-td-desig" class="form-input" required />
                  </div>
                </div>

                <button type="submit" class="btn btn-primary">
                  Save Organization Settings
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();
    await this.loadAdminData();
    await this.loadMasterRecords();
    await this.loadOrgSettings();
  },

  switchTab(tabName) {
    const masterTab = document.getElementById('admin-tab-content-master');
    const subsTab = document.getElementById('admin-tab-content-submissions');
    const settingsTab = document.getElementById('admin-tab-content-settings');

    const btnMaster = document.getElementById('admin-tab-btn-master');
    const btnSubs = document.getElementById('admin-tab-btn-submissions');
    const btnSettings = document.getElementById('admin-tab-btn-settings');

    masterTab.style.display = tabName === 'master' ? 'block' : 'none';
    subsTab.style.display = tabName === 'submissions' ? 'block' : 'none';
    settingsTab.style.display = tabName === 'settings' ? 'block' : 'none';

    btnMaster.className = tabName === 'master' ? 'btn btn-primary btn-sm' : 'btn btn-outline btn-sm';
    btnSubs.className = tabName === 'submissions' ? 'btn btn-primary btn-sm' : 'btn btn-outline btn-sm';
    btnSettings.className = tabName === 'settings' ? 'btn btn-primary btn-sm' : 'btn btn-outline btn-sm';
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
        if (document.getElementById('stat-students')) document.getElementById('stat-students').innerText = statsRes.stats.total_students;
        if (document.getElementById('stat-apps')) document.getElementById('stat-apps').innerText = statsRes.stats.total_applications;
        if (document.getElementById('stat-pending')) document.getElementById('stat-pending').innerText = statsRes.stats.pending_reviews;
        if (document.getElementById('stat-certs')) document.getElementById('stat-certs').innerText = statsRes.stats.issued_certificates;
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

  async loadMasterRecords() {
    try {
      const res = await API.request('/api/admin/master-records');
      const container = document.getElementById('master-records-table-container');
      if (!container) return;

      const records = res.master_records || [];
      if (document.getElementById('stat-master-recs')) {
        document.getElementById('stat-master-recs').innerText = records.length;
      }

      if (records.length === 0) {
        container.innerHTML = `
          <div style="text-align: center; padding: 40px; background: #F8FAFC; border-radius: var(--radius-md); border: 1px dashed var(--color-border);">
            <p style="color: var(--color-gray-text); margin-bottom: 16px;">No Master Internship Records found.</p>
            <button onclick="AdminView.openMasterFormModal()" class="btn btn-primary btn-sm">+ Create First Master Record</button>
          </div>
        `;
        return;
      }

      container.innerHTML = `
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
              <tr style="background: #F1F5F9; border-bottom: 2px solid var(--color-border); text-align: left;">
                <th style="padding: 12px;">Student Name</th>
                <th style="padding: 12px;">College</th>
                <th style="padding: 12px;">Position</th>
                <th style="padding: 12px;">Dates & Duration</th>
                <th style="padding: 12px;">Project</th>
                <th style="padding: 12px;">Mentor</th>
                <th style="padding: 12px;">Offer / Cert ID</th>
                <th style="padding: 12px; text-align: center;">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${records.map(r => `
                <tr style="border-bottom: 1px solid var(--color-border);">
                  <td style="padding: 12px; font-weight: 700; color: var(--color-blue-dark);">${r.student_full_name}</td>
                  <td style="padding: 12px; color: var(--color-gray-text);">${r.college_name}</td>
                  <td style="padding: 12px; font-weight: 600; color: var(--color-accent-blue);">${r.internship_position}</td>
                  <td style="padding: 12px; font-size: 12px;">${r.internship_start_date} - ${r.internship_end_date}<br/><strong style="color: #10B981;">(${r.internship_duration})</strong></td>
                  <td style="padding: 12px; font-size: 12px; max-width: 160px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${r.project_title}">${r.project_title}</td>
                  <td style="padding: 12px;">${r.mentor_name}</td>
                  <td style="padding: 12px; font-size: 11px; font-family: monospace;">
                    Offer: <span style="color: #0B3D91;">${r.offer_id}</span><br/>
                    Cert: <span style="color: #10B981;">${r.certificate_id}</span>
                  </td>
                  <td style="padding: 12px; text-align: center;">
                    <div style="display: flex; gap: 6px; justify-content: center; flex-wrap: wrap;">
                      <button onclick="AdminView.openPreviewModal('${r.id}')" class="btn btn-primary btn-sm" style="padding: 4px 8px; font-size: 11px;">
                        👁️ Preview
                      </button>
                      <button onclick="AdminView.openMasterFormModal('${r.id}')" class="btn btn-outline btn-sm" style="padding: 4px 8px; font-size: 11px;">
                        ✏️ Edit
                      </button>
                    </div>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } catch (e) {
      console.error("Load master records error:", e);
    }
  },

  async loadOrgSettings() {
    try {
      const res = await API.request('/api/admin/organization-settings');
      const org = res.organization_settings || {};
      if (document.getElementById('org-name')) document.getElementById('org-name').value = org.organization_name || 'WebIntern';
      if (document.getElementById('org-website')) document.getElementById('org-website').value = org.organization_website || 'www.webintern.in';
      if (document.getElementById('org-email')) document.getElementById('org-email').value = org.organization_email || 'webinternsupport@gmail.com';
      if (document.getElementById('org-address')) document.getElementById('org-address').value = org.organization_address || 'Virtual Learning Platform';
      if (document.getElementById('org-founder-name')) document.getElementById('org-founder-name').value = org.founder_name || 'Founding Board';
      if (document.getElementById('org-founder-desig')) document.getElementById('org-founder-desig').value = org.founder_designation || 'Founder';
      if (document.getElementById('org-td-name')) document.getElementById('org-td-name').value = org.technical_director_name || 'Dr. A. K. Sharma';
      if (document.getElementById('org-td-desig')) document.getElementById('org-td-desig').value = org.technical_director_designation || 'Technical Director';
    } catch (e) {
      console.error("Load org settings error:", e);
    }
  },

  async saveOrgSettings(e) {
    e.preventDefault();
    const data = {
      organization_name: document.getElementById('org-name').value.trim(),
      organization_website: document.getElementById('org-website').value.trim(),
      organization_email: document.getElementById('org-email').value.trim(),
      organization_address: document.getElementById('org-address').value.trim(),
      founder_name: document.getElementById('org-founder-name').value.trim(),
      founder_designation: document.getElementById('org-founder-desig').value.trim(),
      technical_director_name: document.getElementById('org-td-name').value.trim(),
      technical_director_designation: document.getElementById('org-td-desig').value.trim()
    };

    try {
      Toast.show('Saving Organization Settings...', 'info');
      const res = await API.request('/api/admin/organization-settings', {
        method: 'POST',
        body: data
      });
      Toast.show(res.message || 'Settings saved successfully!', 'success');
    } catch (err) {
      Toast.show(err.message || 'Failed to save organization settings.', 'error');
    }
  },

  async openMasterFormModal(recordId = None) {
    let rec = null;
    if (recordId) {
      try {
        const res = await API.request(`/api/admin/master-records/${recordId}`);
        rec = res.master_record;
      } catch (e) {
        Toast.show('Failed to load master record.', 'error');
        return;
      }
    }

    const isEdit = !!rec;
    const title = isEdit ? `Edit Master Record: ${rec.student_full_name}` : 'Create Master Internship Record';

    const html = `
      <div style="max-width: 780px; max-height: 85vh; overflow-y: auto; padding-right: 8px;">
        <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 4px;">${title}</h2>
        <p style="font-size: 13px; color: var(--color-gray-text); margin-bottom: 20px;">
          Single Source-of-Truth form. Data entered here populates both Offer Letter and Certificate without duplicate entry.
        </p>

        <form id="master-record-form" onsubmit="AdminView.submitMasterRecord(event, '${isEdit ? rec.id : ''}')">
          <!-- Section 1: Student Information -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 18px;">
            <h3 style="font-size: 15px; color: var(--color-blue-dark); margin-bottom: 12px;">1. Student Information</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div>
                <label class="form-label">Student Full Name *</label>
                <input type="text" id="m-student-name" class="form-input" value="${rec ? rec.student_full_name : ''}" required placeholder="e.g. MOHAN ENI" />
              </div>
              <div>
                <label class="form-label">Student Email *</label>
                <input type="email" id="m-student-email" class="form-input" value="${rec ? rec.student_email : ''}" required placeholder="student@gmail.com" />
              </div>
              <div>
                <label class="form-label">Mobile Number</label>
                <input type="text" id="m-student-mobile" class="form-input" value="${rec ? (rec.student_mobile || '') : ''}" placeholder="9876543210" />
              </div>
              <div>
                <label class="form-label">Student ID / Roll Number</label>
                <input type="text" id="m-student-id" class="form-input" value="${rec ? (rec.student_id || '') : ''}" placeholder="WI20260001" />
              </div>
            </div>
          </div>

          <!-- Section 2: Academic Information -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 18px;">
            <h3 style="font-size: 15px; color: var(--color-blue-dark); margin-bottom: 12px;">2. Academic Information</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div>
                <label class="form-label">College Name *</label>
                <input type="text" id="m-college-name" class="form-input" value="${rec ? rec.college_name : ''}" required placeholder="e.g. Karpagam Institute of Technology" />
              </div>
              <div>
                <label class="form-label">University Name</label>
                <input type="text" id="m-university-name" class="form-input" value="${rec ? (rec.university_name || '') : ''}" placeholder="e.g. Anna University" />
              </div>
              <div>
                <label class="form-label">Degree *</label>
                <input type="text" id="m-degree" class="form-input" value="${rec ? rec.degree : 'B.E.'}" required placeholder="e.g. B.E. / B.Tech" />
              </div>
              <div>
                <label class="form-label">Department *</label>
                <input type="text" id="m-department" class="form-input" value="${rec ? rec.department : ''}" required placeholder="e.g. Electrical and Electronics Engineering" />
              </div>
            </div>
          </div>

          <!-- Section 3: Internship Information -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 18px;">
            <h3 style="font-size: 15px; color: var(--color-blue-dark); margin-bottom: 12px;">3. Internship Information</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div>
                <label class="form-label">Internship Position / Role *</label>
                <input type="text" id="m-position" class="form-input" value="${rec ? rec.internship_position : ''}" required placeholder="e.g. Software Development Intern" />
              </div>
              <div>
                <label class="form-label">Execution Mode</label>
                <select id="m-mode" class="form-input">
                  <option value="Online" ${rec && rec.internship_mode === 'Online' ? 'selected' : ''}>Online / Virtual</option>
                  <option value="Hybrid" ${rec && rec.internship_mode === 'Hybrid' ? 'selected' : ''}>Hybrid</option>
                  <option value="Onsite" ${rec && rec.internship_mode === 'Onsite' ? 'selected' : ''}>Onsite</option>
                </select>
              </div>
              <div>
                <label class="form-label">Start Date *</label>
                <input type="text" id="m-start-date" class="form-input" value="${rec ? rec.internship_start_date : 'September 06, 2026'}" required placeholder="September 06, 2026" onchange="AdminView.autoCalculateDuration()" />
              </div>
              <div>
                <label class="form-label">End Date *</label>
                <input type="text" id="m-end-date" class="form-input" value="${rec ? rec.internship_end_date : 'October 04, 2026'}" required placeholder="October 04, 2026" onchange="AdminView.autoCalculateDuration()" />
              </div>
            </div>
          </div>

          <!-- Section 4: Project Information -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 18px;">
            <h3 style="font-size: 15px; color: var(--color-blue-dark); margin-bottom: 12px;">4. Project Information</h3>
            <div>
              <label class="form-label">Project Title *</label>
              <input type="text" id="m-project-title" class="form-input" value="${rec ? rec.project_title : ''}" required placeholder="e.g. Full-Stack Enterprise Web Application Capstone" />
            </div>
          </div>

          <!-- Section 5: Mentor Information -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 18px;">
            <h3 style="font-size: 15px; color: var(--color-blue-dark); margin-bottom: 12px;">5. Mentor / Supervisor Information</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
              <div>
                <label class="form-label">Mentor Name *</label>
                <input type="text" id="m-mentor-name" class="form-input" value="${rec ? rec.mentor_name : 'Dr. A. Karthik'}" required placeholder="e.g. Dr. A. Karthik" />
              </div>
              <div>
                <label class="form-label">Mentor Designation</label>
                <input type="text" id="m-mentor-desig" class="form-input" value="${rec ? (rec.mentor_designation || 'Technical Mentor') : 'Technical Mentor'}" placeholder="Technical Mentor" />
              </div>
            </div>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px;">
            <button type="button" onclick="Modals.close()" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-primary">${isEdit ? 'Save Master Record Changes' : 'Create Master Record'}</button>
          </div>
        </form>
      </div>
    `;

    Modals.open(html);
  },

  async submitMasterRecord(e, recordId) {
    e.preventDefault();
    const data = {
      student_full_name: document.getElementById('m-student-name').value.trim(),
      student_email: document.getElementById('m-student-email').value.trim(),
      student_mobile: document.getElementById('m-student-mobile').value.trim(),
      student_id: document.getElementById('m-student-id').value.trim(),
      college_name: document.getElementById('m-college-name').value.trim(),
      university_name: document.getElementById('m-university-name').value.trim(),
      degree: document.getElementById('m-degree').value.trim(),
      department: document.getElementById('m-department').value.trim(),
      internship_position: document.getElementById('m-position').value.trim(),
      internship_mode: document.getElementById('m-mode').value,
      internship_start_date: document.getElementById('m-start-date').value.trim(),
      internship_end_date: document.getElementById('m-end-date').value.trim(),
      project_title: document.getElementById('m-project-title').value.trim(),
      mentor_name: document.getElementById('m-mentor-name').value.trim(),
      mentor_designation: document.getElementById('m-mentor-desig').value.trim()
    };

    try {
      Toast.show('Saving Master Internship Record...', 'info');
      const url = recordId ? `/api/admin/master-records/${recordId}` : '/api/admin/master-records';
      const method = recordId ? 'PUT' : 'POST';
      const res = await API.request(url, { method, body: data });

      Toast.show(res.message || 'Master Record saved successfully!', 'success');
      Modals.close();
      this.loadMasterRecords();
    } catch (err) {
      if (err.data && err.data.validation_errors) {
        Toast.show(err.data.validation_errors.join(' '), 'error');
      } else {
        Toast.show(err.message || 'Failed to save master record.', 'error');
      }
    }
  },

  async openPreviewModal(recordId) {
    try {
      const recRes = await API.request(`/api/admin/master-records/${recordId}`);
      const rec = recRes.master_record;

      const html = `
        <div style="max-width: 680px; font-family: inherit;">
          <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 6px;">Master Record & Document Preview</h2>
          <p style="font-size: 13px; color: var(--color-gray-text); margin-bottom: 20px;">
            Structured data mapping summary from the single source-of-truth master record.
          </p>

          <!-- Structured Summary Box -->
          <div style="background: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 24px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px;">
              <div><strong>STUDENT:</strong> <span style="color: #082B66; font-weight:700;">${rec.student_full_name}</span></div>
              <div><strong>COLLEGE:</strong> <span>${rec.college_name}</span></div>
              <div><strong>UNIVERSITY:</strong> <span>${rec.university_name || 'N/A'}</span></div>
              <div><strong>INTERNSHIP:</strong> <span style="color: #0B3D91; font-weight:700;">${rec.internship_position}</span></div>
              <div><strong>START DATE:</strong> <span>${rec.internship_start_date}</span></div>
              <div><strong>END DATE:</strong> <span>${rec.internship_end_date}</span></div>
              <div><strong>DURATION:</strong> <span style="color: #10B981; font-weight:700;">${rec.internship_duration}</span></div>
              <div><strong>MENTOR:</strong> <span>${rec.mentor_name}</span></div>
              <div style="grid-column: span 2;"><strong>PROJECT:</strong> <span>${rec.project_title}</span></div>
              <div><strong>OFFER ID:</strong> <span style="font-family: monospace;">${rec.offer_id}</span></div>
              <div><strong>CERTIFICATE ID:</strong> <span style="font-family: monospace;">${rec.certificate_id}</span></div>
            </div>
          </div>

          <!-- Document Action Buttons -->
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; gap: 10px;">
              <a href="/api/admin/master-records/${rec.id}/generate-offer" target="_blank" class="btn btn-primary" style="flex: 1; text-align: center;">
                📄 Generate & View Offer Letter PDF
              </a>
              <a href="/api/admin/master-records/${rec.id}/generate-certificate" target="_blank" class="btn btn-primary" style="flex: 1; text-align: center; background: #10B981; border-color: #10B981;">
                🎓 Generate & View Certificate PDF
              </a>
            </div>
            <button onclick="Modals.close()" class="btn btn-outline">Close Preview</button>
          </div>
        </div>
      `;

      Modals.open(html);
    } catch (e) {
      Toast.show('Failed to load record preview.', 'error');
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

