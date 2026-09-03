// Auth Views Renderer (Create Account & Login with Supabase, Email/Password, Google OAuth — Direct Sign-In without compulsory OTP)

const GOOGLE_BTN_HTML = `
  <div style="display: flex; align-items: center; margin: 20px 0; text-align: center;">
    <div style="flex-grow: 1; border-bottom: 1px solid var(--color-border);"></div>
    <span style="padding: 0 12px; font-size: 13px; color: var(--color-gray-text); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;">or</span>
    <div style="flex-grow: 1; border-bottom: 1px solid var(--color-border);"></div>
  </div>

  <button type="button" id="google-signin-btn" class="btn btn-full" style="
    background-color: #FFFFFF;
    color: #3C4043;
    border: 1px solid #DADCE0;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 14px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: background-color 0.2s, box-shadow 0.2s;
    cursor: pointer;
  " onmouseover="this.style.backgroundColor='#F8F9FA'; this.style.boxShadow='0 2px 6px rgba(0,0,0,0.12)';" onmouseout="this.style.backgroundColor='#FFFFFF'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)';">
    <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
      <path fill="#4285F4" d="M17.64 9.2c0-.74-.06-1.28-.19-1.84H9v3.34h4.96c-.1.83-.64 2.08-1.84 2.92l2.84 2.2c1.7-1.57 2.68-3.88 2.68-6.62z"/>
      <path fill="#34A853" d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.84-2.2c-.76.53-1.78.9-3.12.9-2.38 0-4.41-1.57-5.13-3.72L.97 13.01C2.45 15.96 5.48 18 9 18z"/>
      <path fill="#FBBC05" d="M3.87 10.8c-.2-.58-.31-1.21-.31-1.8s.11-1.22.31-1.8L.97 4.99C.35 6.22 0 7.6 0 9s.35 2.78.97 4.01l2.9-2.21z"/>
      <path fill="#EA4335" d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.59C13.46.89 11.43 0 9 0 5.48 0 2.45 2.04.97 4.99l2.9 2.21C4.59 5.05 6.62 3.58 9 3.58z"/>
    </svg>
    <span>Continue with Google</span>
  </button>
`;

const AuthViews = {
  renderRegister() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg); min-height: calc(100vh - 72px); display: flex; align-items: center; justify-content: center;">
        <div class="container" style="max-width: 500px;">
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 40px 32px; border: 1px solid var(--color-border); box-shadow: var(--shadow-xl);">
            
            <div style="text-align: center; margin-bottom: 24px;">
              <img src="/assets/logo.svg" alt="Web Intern" height="36" style="margin: 0 auto 16px auto;" />
              <h1 style="font-size: 26px; color: var(--color-blue-dark); margin-bottom: 6px;">Create your account</h1>
              <p style="color: var(--color-gray-text); font-size: 14px;">Register to start your virtual internship program.</p>
            </div>

            <!-- Direct Account Registration Form -->
            <form id="register-form">
              <div class="form-group">
                <label class="form-label">Full Name *</label>
                <div style="position: relative;">
                  <i data-feather="user" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="text" id="reg-name" class="form-input" style="padding-left: 42px;" placeholder="John Doe" required />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Email Address *</label>
                <div style="position: relative;">
                  <i data-feather="mail" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="email" id="reg-email" class="form-input" style="padding-left: 42px;" placeholder="you@example.com" required />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Mobile Number</label>
                <div style="display: flex; gap: 8px;">
                  <select id="reg-country-code" class="form-input" style="width: 110px; padding: 12px 8px; font-size: 13px;">
                    <option value="+91">+91 — IN</option>
                    <option value="+1">+1 — US</option>
                    <option value="+44">+44 — UK</option>
                    <option value="+61">+61 — AU</option>
                    <option value="+971">+971 — AE</option>
                  </select>
                  <div style="position: relative; flex-grow: 1;">
                    <i data-feather="phone" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                    <input type="tel" id="reg-phone" class="form-input" style="padding-left: 42px;" placeholder="9876543210" />
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Password *</label>
                <div style="position: relative;">
                  <i data-feather="lock" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="password" id="reg-password" class="form-input" style="padding-left: 42px;" placeholder="Minimum 6 characters" minlength="6" required />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Confirm Password *</label>
                <div style="position: relative;">
                  <i data-feather="lock" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="password" id="reg-confirm-password" class="form-input" style="padding-left: 42px;" placeholder="Re-enter password" minlength="6" required />
                </div>
              </div>

              <div style="margin-bottom: 20px; display: flex; flex-direction: column; gap: 12px;">
                <label class="checkbox-label">
                  <input type="checkbox" id="reg-terms" required />
                  <span>I agree to the <a href="#/privacy-policy" target="_blank" style="color: var(--color-accent-blue);">Terms & Conditions</a> and <a href="#/privacy-policy" target="_blank" style="color: var(--color-accent-blue);">Privacy Policy</a> *</span>
                </label>

                <label class="checkbox-label">
                  <input type="checkbox" id="reg-marketing" />
                  <span>Send me updates, offers and marketing emails</span>
                </label>
              </div>

              <button type="submit" id="reg-submit-btn" class="btn btn-primary btn-full btn-lg" style="border-radius: 9999px;">
                Create Account
              </button>
            </form>

            ${GOOGLE_BTN_HTML}

            <div style="text-align: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--color-border);">
              <span style="font-size: 14px; color: var(--color-gray-text);">Already have an account? </span>
              <a href="#/login" style="font-weight: 600; color: var(--color-accent-blue);">Sign In</a>
            </div>

          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();
    this.bindRegisterEvents();
    this.bindGoogleAuthEvent();
  },

  bindRegisterEvents() {
    const form = document.getElementById('register-form');

    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const phone = document.getElementById('reg-phone').value.trim();
      const countryCode = document.getElementById('reg-country-code').value;
      const password = document.getElementById('reg-password').value;
      const confirmPassword = document.getElementById('reg-confirm-password').value;
      const terms = document.getElementById('reg-terms').checked;
      const marketing = document.getElementById('reg-marketing').checked;

      if (password !== confirmPassword) {
        Toast.show('Passwords do not match.', 'error');
        return;
      }

      if (!terms) {
        Toast.show('You must agree to the Terms & Conditions.', 'error');
        return;
      }

      const submitBtn = document.getElementById('reg-submit-btn');
      try {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Creating account...';

        const res = await API.request('/api/auth/register', {
          method: 'POST',
          body: {
            full_name: name,
            email,
            phone,
            phone_country_code: countryCode,
            password,
            confirm_password: confirmPassword,
            terms_accepted: terms,
            marketing_opt_in: marketing
          }
        });

        API.setAuthToken(res.token);
        API.setCurrentUser(res.user);
        HeaderComponent.updateAuthState();

        Toast.show('Account created successfully! Welcome to WebIntern.', 'success');
        window.location.hash = '#/dashboard';
      } catch (err) {
        Toast.show(err.message, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Create Account';
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
              <p style="color: var(--color-gray-text); font-size: 14px;">Sign in to access your WebIntern dashboard.</p>
            </div>

            <!-- Email & Password Login Form -->
            <form id="login-form">
              <div class="form-group">
                <label class="form-label">Email Address</label>
                <div style="position: relative;">
                  <i data-feather="mail" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="email" id="login-email" class="form-input" style="padding-left: 42px;" placeholder="you@example.com" required />
                </div>
              </div>

              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <label class="form-label" style="margin-bottom: 0;">Password</label>
                  <a href="javascript:void(0)" onclick="AuthViews.handleForgotPassword()" style="font-size: 13px; color: var(--color-accent-blue); font-weight: 500;">Forgot password?</a>
                </div>
                <div style="position: relative;">
                  <i data-feather="lock" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--color-gray-text); width: 18px;"></i>
                  <input type="password" id="login-password" class="form-input" style="padding-left: 42px;" placeholder="Enter your password" required />
                </div>
              </div>

              <button type="submit" id="login-submit-btn" class="btn btn-primary btn-full btn-lg" style="border-radius: 9999px;">
                Sign In
              </button>
            </form>

            ${GOOGLE_BTN_HTML}

            <div style="text-align: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--color-border);">
              <span style="font-size: 14px; color: var(--color-gray-text);">New to Web Intern? </span>
              <a href="#/register" style="font-weight: 600; color: var(--color-accent-blue);">Create an account</a>
            </div>

          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();
    this.bindLoginEvents();
    this.bindGoogleAuthEvent();
  },

  bindLoginEvents() {
    const form = document.getElementById('login-form');

    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const password = document.getElementById('login-password').value;
      const submitBtn = document.getElementById('login-submit-btn');

      try {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Signing in...';

        const res = await API.request('/api/auth/login', {
          method: 'POST',
          body: { email, password }
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
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Sign In';
      }
    });
  },

  bindGoogleAuthEvent() {
    const googleBtn = document.getElementById('google-signin-btn');
    googleBtn?.addEventListener('click', async () => {
      try {
        const authConfig = await API.request('/api/auth/config');
        const clientId = authConfig.google_client_id;
        
        if (!clientId) {
          Toast.show('Google Client ID is not configured.', 'error');
          return;
        }
        
        // Option A: Official Google Identity Services Popup (GIS Token Client)
        if (window.google?.accounts?.oauth2) {
          const client = window.google.accounts.oauth2.initTokenClient({
            client_id: clientId,
            scope: 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
            callback: async (tokenResponse) => {
              if (tokenResponse.error) {
                Toast.show(`Google login cancelled: ${tokenResponse.error}`, 'error');
                return;
              }
              try {
                Toast.show('Authenticating with Google...', 'info');
                const res = await API.request('/api/auth/google-sync', {
                  method: 'POST',
                  body: { access_token: tokenResponse.access_token }
                });

                API.setAuthToken(res.token);
                API.setCurrentUser(res.user);
                HeaderComponent.updateAuthState();

                Toast.show('Signed in with Google successfully!', 'success');
                window.location.hash = '#/dashboard';
              } catch (err) {
                Toast.show(err.message || 'Google authentication failed.', 'error');
              }
            }
          });
          client.requestAccessToken();
          return;
        }

        // Option B: Supabase OAuth if initialized
        const supabase = await API.getSupabase();
        if (supabase) {
          const redirectUrl = window.location.origin + '/#/';
          const { error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: { redirectTo: redirectUrl }
          });
          if (!error) return;
        }

        // Option C: Standard Google OAuth Redirect
        const redirectUri = encodeURIComponent(window.location.origin + '/oauth2callback');
        const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=openid%20email%20profile`;
        window.location.href = googleAuthUrl;

      } catch (err) {
        Toast.show(`Google Sign-In error: ${err.message}`, 'error');
      }
    });
  },

  async checkGoogleOAuthCallback() {
    try {
      const supabase = await API.getSupabase();
      if (!supabase) return;

      const { data: { session } } = await supabase.auth.getSession();
      if (session && session.user) {
        const googleUser = session.user;
        const res = await API.request('/api/auth/google-sync', {
          method: 'POST',
          body: {
            id: googleUser.id,
            email: googleUser.email,
            name: googleUser.user_metadata?.full_name || googleUser.user_metadata?.name || ''
          }
        });

        API.setAuthToken(res.token);
        API.setCurrentUser(res.user);
        HeaderComponent.updateAuthState();

        Toast.show('Signed in with Google successfully!', 'success');
        window.location.hash = '#/dashboard';
      }
    } catch (e) {
      console.warn('Google OAuth session check:', e);
    }
  },

  async handleForgotPassword() {
    const email = prompt('Enter your registered email address to receive a password reset link:');
    if (!email || !email.trim()) return;

    try {
      Toast.show('Sending password reset email via Resend...', 'info');
      const res = await API.request('/api/auth/forgot-password', {
        method: 'POST',
        body: { email: email.trim() }
      });
      Toast.show(res.message, 'success');
    } catch (err) {
      Toast.show(err.message, 'error');
    }
  }
};
