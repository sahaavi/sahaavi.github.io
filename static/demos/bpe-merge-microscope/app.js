const state = {
  data: null,
  currentStep: 0,
};

const els = {
  slider: document.querySelector("#step-slider"),
  stepLabel: document.querySelector("#step-label"),
  selectedPair: document.querySelector("#selected-pair"),
  vocabSize: document.querySelector("#vocab-size"),
  totalTokens: document.querySelector("#total-tokens"),
  compression: document.querySelector("#compression"),
  before: document.querySelector("#before-sequences"),
  after: document.querySelector("#after-sequences"),
  pairCounts: document.querySelector("#pair-counts"),
  tryText: document.querySelector("#try-text"),
  encodedOutput: document.querySelector("#encoded-output"),
};

function pieceText(piece) {
  return piece.text || bytesToText(piece.bytes || []);
}

function bytesEqual(left, right) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function bytesToText(bytes) {
  const decoded = new TextDecoder("utf-8", { fatal: false }).decode(new Uint8Array(bytes));
  if (decoded.includes("\uFFFD")) {
    return "0x" + bytes.map((byte) => byte.toString(16).padStart(2, "0")).join("");
  }
  return decoded.replaceAll(" ", "␠").replaceAll("\n", "\\n");
}

function renderSequences(target, sequences, selectedPair) {
  target.innerHTML = "";
  sequences.forEach((sequence) => {
    const row = document.createElement("div");
    row.className = "sequence-row";
    sequence.forEach((piece, index) => {
      const tile = document.createElement("span");
      tile.className = "tile";
      const isSelected =
        selectedPair &&
        index + 1 < sequence.length &&
        bytesEqual(piece.bytes, selectedPair[0].bytes) &&
        bytesEqual(sequence[index + 1].bytes, selectedPair[1].bytes);
      if (isSelected) tile.classList.add("selected");
      tile.textContent = pieceText(piece);
      row.appendChild(tile);
    });
    target.appendChild(row);
  });
}

function renderPairCounts(pairs) {
  els.pairCounts.innerHTML = "";
  pairs.forEach((pair) => {
    const item = document.createElement("li");
    item.innerHTML = `<strong>${pieceText(pair.left)} + ${pieceText(pair.right)}</strong>: ${pair.count}`;
    els.pairCounts.appendChild(item);
  });
}

function mergeSequence(sequence, merge) {
  const output = [];
  let index = 0;
  while (index < sequence.length) {
    if (
      index + 1 < sequence.length &&
      bytesEqual(sequence[index], merge.left.bytes) &&
      bytesEqual(sequence[index + 1], merge.right.bytes)
    ) {
      output.push(merge.token.bytes);
      index += 2;
    } else {
      output.push(sequence[index]);
      index += 1;
    }
  }
  return output;
}

function encodeText(text) {
  let sequence = Array.from(new TextEncoder().encode(text), (byte) => [byte]);
  state.data.merges.forEach((merge) => {
    sequence = mergeSequence(sequence, merge);
  });
  return sequence;
}

function renderTryEncode() {
  const pieces = encodeText(els.tryText.value);
  els.encodedOutput.innerHTML = "";
  pieces.forEach((bytes) => {
    const tile = document.createElement("span");
    tile.className = "tile";
    tile.textContent = bytesToText(bytes);
    els.encodedOutput.appendChild(tile);
  });
}

function renderStep(stepIndex) {
  const step = state.data.steps[stepIndex];
  state.currentStep = stepIndex;
  els.stepLabel.textContent = `step ${step.step} / ${state.data.steps.length}`;
  els.selectedPair.textContent = `${pieceText(step.selected_pair[0])} + ${pieceText(step.selected_pair[1])} → ${pieceText(step.merged_token)} (${step.frequency}×)`;
  els.vocabSize.textContent = step.metrics.vocab_size;
  els.totalTokens.textContent = step.metrics.total_tokens;
  els.compression.textContent = step.metrics.compression_ratio.toFixed(2);
  renderSequences(els.before, step.before_sequences, step.selected_pair);
  renderSequences(els.after, step.after_sequences, null);
  renderPairCounts(step.top_pairs);
  renderTryEncode();
}

async function init() {
  const response = await fetch("data.json");
  state.data = await response.json();
  els.slider.max = Math.max(0, state.data.steps.length - 1);
  els.slider.value = 0;
  els.slider.addEventListener("input", (event) => renderStep(Number(event.target.value)));
  els.tryText.addEventListener("input", renderTryEncode);
  renderStep(0);
}

init().catch((error) => {
  document.body.innerHTML = `<pre>Could not load BPE trace: ${error.message}</pre>`;
});
