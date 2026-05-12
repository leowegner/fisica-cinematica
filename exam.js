const V = (l) => `<span class="vec">${l}</span>`;
const VS = (l, s) => `<span class="vec">${l}</span><sub>${s}</sub>`;

const questions = [
  {
    q: "¿Cuáles son los 3 elementos fundamentales para el estudio del movimiento?",
    options: [
      "Masa, fuerza y energía",
      "Móvil, trayectoria y tiempo",
      "Posición, velocidad y aceleración",
      "Espacio, vector y origen"
    ],
    correct: 1,
    explain: "Para estudiar el movimiento necesitamos un móvil (objeto), una trayectoria (línea que describe) y el tiempo."
  },
  {
    q: "¿Qué es la trayectoria?",
    options: [
      "La distancia en línea recta entre dos puntos",
      "El vector que une el origen con el móvil",
      "La línea descrita por un móvil en su movimiento",
      "El cambio de posición respecto al tiempo"
    ],
    correct: 2,
    explain: "La trayectoria es la línea descrita por un móvil durante su movimiento. Puede ser recta (rectilíneo) o curva (curvilíneo)."
  },
  {
    q: "Sobre el movimiento, ¿cuál de estas afirmaciones es CIERTA?",
    options: [
      "Hay movimiento absoluto, no depende del observador",
      "No hay movimiento absoluto, solo relativo a un sistema de referencia",
      "El movimiento solo existe si hay aceleración",
      "Una trayectoria curva implica siempre velocidad constante"
    ],
    correct: 1,
    explain: "El movimiento siempre se mide respecto a un sistema de referencia, por lo que es relativo, no absoluto."
  },
  {
    q: `¿Qué es el vector de posición ${V('r')}?`,
    options: [
      "El vector que une dos posiciones cualesquiera del móvil",
      "Un vector tangente a la trayectoria",
      "El vector cuyo extremo coincide con la posición del móvil y su origen con el origen del sistema de referencia",
      "El vector velocidad en un instante"
    ],
    correct: 2,
    explain: "El vector de posición tiene su punto de aplicación en el origen y su extremo en la posición instantánea del móvil."
  },
  {
    q: "¿Cuál es la diferencia entre desplazamiento y espacio recorrido?",
    options: [
      "Son lo mismo, solo cambia el nombre",
      `El desplazamiento es la línea recta entre dos posiciones (vector ${V('ΔL')}); el espacio recorrido es la longitud real sobre la trayectoria`,
      "El espacio recorrido es siempre menor que el desplazamiento",
      "El desplazamiento es un escalar y el espacio recorrido un vector"
    ],
    correct: 1,
    explain: `Desplazamiento ${V('ΔL')} = línea recta entre A y B (vector). Espacio recorrido = longitud real sobre la trayectoria curva.`
  },
  {
    q: "¿Cómo se define la velocidad?",
    options: [
      "Magnitud escalar que mide la distancia recorrida",
      "Magnitud vectorial que mide la rapidez de los cambios de posición de un móvil",
      "Magnitud vectorial que mide los cambios de aceleración",
      "El producto de la masa por el tiempo"
    ],
    correct: 1,
    explain: "La velocidad es una magnitud VECTORIAL que mide la rapidez con la que cambia la posición de un móvil."
  },
  {
    q: "¿Qué fórmula corresponde a la velocidad media?",
    options: [
      `${VS('v','m')} = v² / R`,
      `${VS('v','m')} = Δ${V('v')} / Δt`,
      `${VS('v','m')} = Δx / Δt = (x<sub>f</sub> − x<sub>0</sub>) / (t<sub>f</sub> − t<sub>0</sub>)`,
      `${VS('v','m')} = d · t`
    ],
    correct: 2,
    explain: "La velocidad media relaciona el cambio de posición Δx con el tiempo empleado Δt."
  },
  {
    q: "¿Qué dirección tiene siempre la velocidad instantánea en un punto de la trayectoria?",
    options: [
      "Perpendicular a la trayectoria",
      "Hacia el centro de la curva",
      "Tangente a la trayectoria en ese punto",
      "Paralela al eje X"
    ],
    correct: 2,
    explain: "La velocidad instantánea siempre es tangente a la trayectoria en cada punto."
  },
  {
    q: `La aceleración tangencial (${VS('a','t')})…`,
    options: [
      "Mide los cambios de dirección de la velocidad",
      "Mide los cambios del módulo de la velocidad y es tangente a la trayectoria",
      "Es siempre perpendicular a la velocidad",
      "Apunta siempre hacia el centro de la curva"
    ],
    correct: 1,
    explain: "La aceleración tangencial mide cambios en el MÓDULO (rapidez) de la velocidad. Su dirección es tangente a la trayectoria."
  },
  {
    q: `La aceleración centrípeta (${VS('a','c')})…`,
    options: [
      "Es tangente a la trayectoria",
      `Vale ${VS('a','c')} = Δ${V('v')}/Δt`,
      `Es perpendicular a la trayectoria, apunta al centro de la curva y vale ${VS('a','c')} = v²/R`,
      "Solo existe en movimiento rectilíneo"
    ],
    correct: 2,
    explain: `La aceleración centrípeta mide los cambios de DIRECCIÓN de la velocidad. Es perpendicular a la trayectoria, dirigida al centro de la curva: ${VS('a','c')} = v²/R.`
  }
];

const examEl = document.getElementById('exam');
const submitBtn = document.getElementById('submitBtn');
const resetBtn = document.getElementById('resetBtn');
const resultEl = document.getElementById('result');

function renderExam() {
  examEl.innerHTML = questions.map((q, i) => `
    <div class="question" data-q="${i}">
      <span class="q-num">Pregunta ${i + 1}</span>
      <p class="q-text">${q.q}</p>
      <div class="options">
        ${q.options.map((opt, j) => `
          <label data-opt="${j}">
            <input type="radio" name="q${i}" value="${j}">
            <span>${opt}</span>
          </label>
        `).join('')}
      </div>
    </div>
  `).join('');

  examEl.querySelectorAll('.options label').forEach(label => {
    label.addEventListener('click', () => {
      const parent = label.closest('.options');
      parent.querySelectorAll('label').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
    });
  });
}

function correct() {
  let score = 0;
  questions.forEach((q, i) => {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    const labels = examEl.querySelectorAll(`.question[data-q="${i}"] .options label`);
    labels.forEach(l => l.classList.remove('correct', 'wrong'));

    const correctLabel = examEl.querySelector(`.question[data-q="${i}"] .options label[data-opt="${q.correct}"]`);
    correctLabel.classList.add('correct');

    if (selected) {
      const chosen = parseInt(selected.value);
      if (chosen === q.correct) {
        score++;
      } else {
        const wrongLabel = examEl.querySelector(`.question[data-q="${i}"] .options label[data-opt="${chosen}"]`);
        wrongLabel.classList.add('wrong');
      }
    }

    const questionEl = examEl.querySelector(`.question[data-q="${i}"]`);
    if (!questionEl.querySelector('.explanation')) {
      const exp = document.createElement('div');
      exp.className = 'explanation';
      exp.innerHTML = `<strong>Explicación:</strong> ${q.explain}`;
      questionEl.appendChild(exp);
    }
  });

  const pct = Math.round((score / questions.length) * 100);
  let msg = '';
  let cls = '';
  if (pct >= 80) { msg = '¡Excelente! Dominas la cinemática.'; cls = 'good'; }
  else if (pct >= 50) { msg = 'Buen trabajo, pero repasa los conceptos que has fallado.'; cls = ''; }
  else { msg = 'Te toca repasar los apuntes. Lee de nuevo las secciones y vuelve a intentarlo.'; cls = 'bad'; }

  resultEl.className = `result ${cls}`;
  resultEl.innerHTML = `
    <div class="score">${score} / ${questions.length}</div>
    <p>Acertaste el <strong>${pct}%</strong>. ${msg}</p>
  `;
  resultEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function reset() {
  renderExam();
  resultEl.className = 'result hidden';
  window.scrollTo({ top: document.getElementById('examen').offsetTop - 20, behavior: 'smooth' });
}

submitBtn.addEventListener('click', correct);
resetBtn.addEventListener('click', reset);

renderExam();
