// Global Modal & Razorpay Checkout Controller
const Modals = {
  open(htmlContent) {
    const overlay = document.getElementById('global-modal-overlay');
    const content = document.getElementById('global-modal-content');
    if (!overlay || !content) return;

    content.innerHTML = `
      <button class="modal-close-btn" onclick="Modals.close()">&times;</button>
      ${htmlContent}
    `;
    overlay.classList.add('open');
    if (window.feather) feather.replace();
  },

  close() {
    const overlay = document.getElementById('global-modal-overlay');
    if (overlay) {
      overlay.classList.remove('open');
    }
  },

  async openRazorpayCheckout(certificateId) {
    try {
      Toast.show('Generating secure payment gateway order...', 'info');
      const orderRes = await API.request('/api/payments/create-order', {
        method: 'POST',
        body: { certificate_id: certificateId }
      });

      const options = {
        key: orderRes.key_id,
        amount: orderRes.amount,
        currency: orderRes.currency,
        name: "Web Intern Platform",
        description: "Verified & Printed Certificate Upgrade",
        order_id: orderRes.order_id,
        handler: async function (response) {
          Toast.show('Verifying transaction signature...', 'info');
          try {
            const verifyRes = await API.request('/api/payments/verify', {
              method: 'POST',
              body: {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                certificate_id: certificateId
              }
            });
            Toast.show(verifyRes.message, 'success');
            if (window.location.hash.startsWith('#/dashboard')) {
              DashboardView.render();
            } else {
              window.location.hash = '#/dashboard';
            }
          } catch (e) {
            Toast.show('Payment verification failed: ' + e.message, 'error');
          }
        },
        prefill: {
          name: API.getCurrentUser()?.name || "",
          email: API.getCurrentUser()?.email || ""
        },
        theme: {
          color: "#0B3D91"
        }
      };

      if (window.Razorpay) {
        const rzp = new Razorpay(options);
        rzp.open();
      } else {
        Toast.show('Razorpay SDK failed to load. Please check internet connection.', 'error');
      }
    } catch (err) {
      Toast.show(err.message || 'Payment initiation failed.', 'error');
    }
  }
};
