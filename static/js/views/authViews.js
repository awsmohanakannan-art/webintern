// Auth Views Renderer (Register & Login with 2 Separate Checkboxes & OTP Step)
const AuthViews = {
  renderRegister() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg); min-height: calc(100vh - 72px); display: flex; align-items: center; justify-content: center;">
        <div class="container" style="max-width: 480px;">
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 40px 32px; border: 1px solid var(--color-border); box-shadow: var(--shadow-xl);">
            
            <div style="text-align: center; margin-bottom: 28px;">
              <img src="/assets/logo.svg" alt="Web Intern" height="36" style="margin: 0 auto 16px auto;" />
              <h1 style="font-size: 26px; color: var(--color-blue-dark); margin-bottom: 6px;">Create your account</h1>
              <p style="color: var(--color-gray-text); font-size: 14px;">Register to start your free virtual internship.</p>
            </div>

            <!-- Registration Form Step 1 -->
            <form id="register-form-step1">
              <div class="form-group">
                <label class="form-label">Full name</label>
                <div style="position: relative;">
                  <i data-feather="user" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="text" id="reg-name" class="form-input" style="padding-left: 42px;" placeholder="Enter your name" required />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Email address</label>
                <div style="position: relative;">
                  <i data-feather="mail" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="email" id="reg-email" class="form-input" style="padding-left: 42px;" placeholder="you@example.com" required />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Mobile number *</label>
                <div style="display: flex; gap: 8px;">
                  <select id="reg-country-code" class="form-input" style="width: 110px; padding: 12px 8px; font-size: 13px;">
                    <option value="+91">+91 — IN</option>
                    <option value="+1">+1 — US</option>
                    <option value="+44">+44 — UK</option>
                  </select>
                  <div style="position: relative; flex-grow: 1;">
                    <i data-feather="phone" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                    <input type="tel" id="reg-phone" class="form-input" style="padding-left: 42px;" placeholder="Enter your mobile number" required />
                  </div>
                </div>
              </div>

              <!-- Two Separate Checkboxes -->
              <div style="margin-bottom: 24px; display: flex; flex-direction: column; gap: 12px;">
                <!-- Checkbox 1: Required Legal Consent -->
                <label class="checkbox-label">
                  <input type="checkbox" id="reg-terms" required />
                  <span>I agree to the <a href="#/privacy-policy" target="_blank" style="color: var(--color-accent-blue);">Terms & Conditions</a> and <a href="#/privacy-policy" target="_blank" style="color: var(--color-accent-blue);">Privacy Policy</a></span>
                </label>

                <!-- Checkbox 2: Optional Marketing Opt-In -->
                <label class="checkbox-label">
                  <input type="checkbox" id="reg-marketing" />
                  <span>Send me updates, offers and marketing emails</span>
                </label>
              </div>

              <button type="submit" class="btn btn-outline btn-full btn-lg">
                <i data-feather="send" style="width: 18px;"></i>
                Send Verification Code
              </button>
            </form>

            <!-- Registration OTP Step 2 (Initially Hidden) -->
            <form id="register-form-step2" style="display: none;">
              <p style="font-size: 14px; color: var(--color-gray-text); text-align: center; margin-bottom: 20px;">
                A 6-digit verification code was sent to <strong id="otp-sent-email-display"></strong>.
              </p>

              <div class="form-group">
                <label class="form-label" style="text-align: center;">Enter 6-Digit Code</label>
                <input type="text" id="reg-otp-code" class="form-input" placeholder="123456" maxlength="6" style="text-align: center; font-size: 24px; font-weight: 700; letter-spacing: 8px;" required />
              </div>

              <button type="submit" class="btn btn-primary btn-full btn-lg" style="margin-bottom: 12px;">
                Verify & Complete Registration
              </button>
              <button type="button" onclick="AuthViews.renderRegister()" class="btn btn-outline btn-full btn-sm">
                ← Change Email / Try Again
              </button>
            </form>

            <div style="text-align: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--color-border);">
              <div style="display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--color-gray-text); margin-bottom: 12px;">
                <i data-feather="shield" style="width: 14px; color: var(--color-primary-blue);"></i>
                Secure sign-up · Your data is protected
              </div>
              <div>
                <span style="font-size: 14px; color: var(--color-gray-text);">Already registered? </span>
                <a href="#/login" style="font-weight: 600; color: var(--color-accent-blue);">Go to Login</a>
              </div>
            </div>

          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    this.bindRegisterEvents();
  },

  bindRegisterEvents() {
    const step1 = document.getElementById('register-form-step1');
    const step2 = document.getElementById('register-form-step2');

    step1?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const phone = document.getElementById('reg-phone').value.trim();
      const terms = document.getElementById('reg-terms').checked;

      try {
        Toast.show('Sending 6-digit OTP code to email...', 'info');
        const res = await API.request('/api/auth/register/request-otp', {
          method: 'POST',
          body: {
            full_name: name,
            email,
            phone,
            terms_accepted: terms
          }
        });

        Toast.show(res.message, 'success');
        if (res.dev_otp) {
          Toast.show(`[DEV OTP CODE]: ${res.dev_otp}`, 'info');
        }

        document.getElementById('otp-sent-email-display').innerText = email;
        step1.style.display = 'none';
        step2.style.display = 'block';
      } catch (err) {
        Toast.show(err.message, 'error');
      }
    });

    step2?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const phone = document.getElementById('reg-phone').value.trim();
      const countryCode = document.getElementById('reg-country-code').value;
      const marketing = document.getElementById('reg-marketing').checked;
      const code = document.getElementById('reg-otp-code').value.trim();

      try {
        Toast.show('Verifying code...', 'info');
        const res = await API.request('/api/auth/register/verify-otp', {
          method: 'POST',
          body: {
            email,
            code,
            full_name: name,
            phone,
            phone_country_code: countryCode,
            marketing_opt_in: marketing
          }
        });

        API.setAuthToken(res.token);
        API.setCurrentUser(res.user);
        HeaderComponent.updateAuthState();
        Toast.show('Account created successfully!', 'success');
        window.location.hash = '#/dashboard';
      } catch (err) {
        Toast.show(err.message, 'error');
      }
    });
  },

  renderLogin() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg); min-height: calc(100vh - 72px); display: flex; align-items: center; justify-content: center;">
        <div class="container" style="max-width: 440px;">
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 40px 32px; border: 1px solid var(--color-border); box-shadow: var(--shadow-xl);">
            
            <div style="text-align: center; margin-bottom: 28px;">
              <img src="/assets/logo.svg" alt="Web Intern" height="36" style="margin: 0 auto 16px auto;" />
              <h1 style="font-size: 26px; color: var(--color-blue-dark); margin-bottom: 6px;">Welcome back</h1>
              <p style="color: var(--color-gray-text); font-size: 14px;">Sign in to continue to your account.</p>
            </div>

            <!-- Student OTP Login Step 1 -->
            <form id="login-form-step1">
              <div class="form-group">
                <label class="form-label">Email address</label>
                <div style="position: relative;">
                  <i data-feather="mail" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="email" id="login-email" class="form-input" style="padding-left: 42px;" placeholder="you@example.com" required />
                </div>
              </div>

              <button type="submit" class="btn btn-outline btn-full btn-lg">
                <i data-feather="send" style="width: 18px;"></i>
                Send Verification Code
              </button>
            </form>

            <!-- Student OTP Login Step 2 -->
            <form id="login-form-step2" style="display: none;">
              <p style="font-size: 14px; color: var(--color-gray-text); text-align: center; margin-bottom: 20px;">
                Enter 6-digit code sent to <strong id="login-otp-email-display"></strong>.
              </p>

              <div class="form-group">
                <input type="text" id="login-otp-code" class="form-input" placeholder="123456" maxlength="6" style="text-align: center; font-size: 24px; font-weight: 700; letter-spacing: 8px;" required />
              </div>

              <button type="submit" class="btn btn-primary btn-full btn-lg" style="margin-bottom: 12px;">
                Verify & Sign In
              </button>
            </form>

            <div style="text-align: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--color-border);">
              <div style="display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--color-gray-text); margin-bottom: 12px;">
                <i data-feather="shield" style="width: 14px; color: var(--color-primary-blue);"></i>
                Secure sign-in · Your data is protected
              </div>
              <div>
                <span style="font-size: 14px; color: var(--color-gray-text);">New to Web Intern? </span>
                <a href="#/register" style="font-weight: 600; color: var(--color-accent-blue);">Create an account</a>
              </div>
            </div>

          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    this.bindLoginEvents();
  },

  bindLoginEvents() {
    const step1 = document.getElementById('login-form-step1');
    const step2 = document.getElementById('login-form-step2');

    step1?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();

      try {
        Toast.show('Sending 6-digit OTP code to email...', 'info');
        const res = await API.request('/api/auth/login/request-otp', {
          method: 'POST',
          body: { email }
        });

        Toast.show(res.message, 'success');
        if (res.dev_otp) {
          Toast.show(`[DEV OTP CODE]: ${res.dev_otp}`, 'info');
        }

        document.getElementById('login-otp-email-display').innerText = email;
        step1.style.display = 'none';
        step2.style.display = 'block';
      } catch (err) {
        Toast.show(err.message, 'error');
      }
    });

    step2?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const code = document.getElementById('login-otp-code').value.trim();

      try {
        Toast.show('Verifying code...', 'info');
        const res = await API.request('/api/auth/login/verify-otp', {
          method: 'POST',
          body: { email, code }
        });

        API.setAuthToken(res.token);
        API.setCurrentUser(res.user);
        HeaderComponent.updateAuthState();
        Toast.show('Login successful!', 'success');

        const params = new URLSearchParams(window.location.hash.split('?')[1] || '');
        const redirect = params.get('redirect');
        window.location.hash = redirect ? decodeURIComponent(redirect) : '#/dashboard';
      } catch (err) {
        Toast.show(err.message, 'error');
      }
    });
  }
};
