(() => {
  const form = document.getElementById('onboarding-form');
  const errEl = document.getElementById('form-error');
  const result = document.getElementById('result');
  const submitBtn = document.getElementById('submit');
  const q = sel => document.querySelector(sel);

  function val(name) {
    const el = form.elements[name];
    if (!el) return undefined;
    if (el.type === 'radio') {
      const checked = form.querySelector(`input[name="${name}"]:checked`);
      return checked ? checked.value : undefined;
    }
    return el.value === '' ? undefined : el.value;
  }

  function num(name) {
    const v = val(name);
    if (v === undefined) return undefined;
    return Number(v);
  }

  function buildPayload() {
    const needMode = val('need_mode');
    const payload = {
      profile: {
        age: num('age'),
        retirement_age: num('retirement_age'),
        investable_assets: num('investable_assets'),
        net_worth: num('net_worth'),
        annual_income_after_tax: num('annual_income_after_tax'),
        annual_essential_spend: num('annual_essential_spend'),
        annual_contribution: num('annual_contribution'),
        total_debt: num('total_debt'),
        annual_debt_service: num('annual_debt_service'),
        emergency_fund_months: num('emergency_fund_months'),
        near_term_liabilities: {
          amount: num('ntl_amount'),
          years_until_due: num('ntl_years'),
          coverage_status: val('ntl_coverage'),
        },
        country: String(val('country') || ''),
        rf_real: num('rf_real') ?? 0.0,
      },
      rt_answers: {
        QRT1: val('QRT1'),
        QRT2: val('QRT2'),
        QRT3: val('QRT3'),
        QRT4: val('QRT4'),
        QRT5: val('QRT5'),
      },
      income_stability: val('income_stability'),
    };
    if (needMode === 'target_spend') {
      payload.target_spend = num('target_spend');
    } else {
      payload.w_target = num('w_target');
    }
    return payload;
  }

  async function postAssessment(payload) {
    const res = await fetch('/api/onboarding/assessment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      credentials: 'same-origin',
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || ('HTTP ' + res.status));
    }
    return res.json();
  }

  function renderResult(data) {
    q('#rs').textContent = (data.rs ?? '—').toFixed ? data.rs.toFixed(1) : data.rs;
    q('#rt').textContent = (data.rt ?? '—').toFixed ? data.rt.toFixed(1) : data.rt;
    q('#rc').textContent = (data.rc ?? '—').toFixed ? data.rc.toFixed(1) : data.rc;
    q('#rn').textContent = (data.rn ?? '—').toFixed ? data.rn.toFixed(1) : data.rn;
    q('#need_gap').textContent = (data.need_gap_pp ?? '—').toFixed ? data.need_gap_pp.toFixed(1) : data.need_gap_pp;
    const anns = Array.isArray(data.annotations) ? data.annotations : [];
    q('#annotations').innerHTML = anns.map(a => `<div>• ${a}</div>`).join('');
    result.classList.remove('hidden');
  }

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    errEl.textContent = '';
    try {
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-60');
      const payload = buildPayload();
      const data = await postAssessment(payload);
      renderResult(data);
      result.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {
      errEl.textContent = 'Fehler beim Absenden: ' + (err.message || String(err));
    }
    submitBtn.disabled = false;
    submitBtn.classList.remove('opacity-60');
  });
})();


