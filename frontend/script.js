const recordButton = document.getElementById('record-button');
const transcriptionTextarea = document.getElementById('transcription');
const geminiResponseTextarea = document.getElementById('gemini-response');
const whisperModelSelect = document.getElementById('whisper-model');
const languageSelect = document.getElementById('transcription-language');
const geminiModelSelect = document.getElementById('gemini-model');
const autoSendCheckbox = document.getElementById('auto-send');

let isRecording = false;
let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener('click', () => {
    if (isRecording) {
        stopRecording();
        recordButton.textContent = 'Start Recording';
        recordButton.classList.remove('recording');
    } else {
        startRecording();
        recordButton.textContent = 'Stop Recording';
        recordButton.classList.add('recording');
    }
    isRecording = !isRecording;
});

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
    mediaRecorder.onstop = sendAudio;
    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
}

async function sendAudio() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('model', whisperModelSelect.value);
    formData.append('language', languageSelect.value);

    try {
        const response = await fetch('/transcribe', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.transcription) {
            transcriptionTextarea.value = data.transcription;
            if (autoSendCheckbox.checked) {
                sendTranscriptionForGeneration(data.transcription);
            }
        } else {
            console.error('Transcription failed:', data.error);
        }
    } catch (error) {
        console.error('Error sending audio:', error);
    } finally {
        audioChunks = [];
    }
}

async function sendTranscriptionForGeneration(transcription) {
    const geminiModel = geminiModelSelect.value;
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcription: transcription,
                model: geminiModel
            })
        });
        const data = await response.json();
        if (data.response) {
            geminiResponseTextarea.value = data.response;
        } else {
            console.error('Generation failed:', data.error);
        }
    } catch (error) {
        console.error('Error sending transcription:', error);
    }
}
