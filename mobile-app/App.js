import React, { useEffect, useMemo, useState } from 'react';
import { SafeAreaView, ScrollView, View, Text, TextInput, Pressable, StyleSheet, Alert, ActivityIndicator, Image, ImageBackground, Linking, Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as FileSystem from 'expo-file-system/legacy';
import * as ImagePicker from 'expo-image-picker';
import * as Sharing from 'expo-sharing';

const STORAGE_KEY = 'hub_podium_beta_state';
const DEFAULT_API_URL = 'http://192.168.15.73:5000';
const RETIRED_API_URLS = ['https://seeker-interior-shake-wifi.trycloudflare.com'];
const APP_BUILD_LABEL = 'beta-upload-v3-2026-05-07';
const MAX_VIDEO_UPLOAD_MB = 2048;
const MAX_VIDEO_UPLOAD_BYTES = MAX_VIDEO_UPLOAD_MB * 1024 * 1024;
const PRIVACY_URL = 'https://hub-podium.com/privacy.html';
const TERMS_URL = 'https://hub-podium.com/terms.html';
const PHOTO_GUIDE_POINTS = [
  'Centralize rosto e ombros',
  'Use fundo neutro e sem objetos',
  'Evite luz forte atrás do atleta'
];
const CATEGORY_OPTIONS = Array.from({ length: 13 }, (_, index) => `sub-${index + 8}`);
const COMPETITION_TRACK_OPTIONS = [
  { value: 'masculino', label: 'Masculino' },
  { value: 'feminino', label: 'Feminino' }
];
const POSITION_OPTIONS = [
  { value: 'goleiro', label: 'Goleiro' },
  { value: 'lateral direito', label: 'Lateral direito' },
  { value: 'zagueiro direito', label: 'Zagueiro direito' },
  { value: 'zagueiro central', label: 'Zagueiro central' },
  { value: 'zagueiro esquerdo', label: 'Zagueiro esquerdo' },
  { value: 'lateral esquerdo', label: 'Lateral esquerdo' },
  { value: 'ala direita', label: 'Ala direita' },
  { value: 'ala esquerda', label: 'Ala esquerda' },
  { value: 'primeiro volante', label: 'Primeiro volante' },
  { value: 'segundo volante', label: 'Segundo volante' },
  { value: 'volante', label: 'Volante' },
  { value: 'meia direita', label: 'Meia direita' },
  { value: 'meia central', label: 'Meia central' },
  { value: 'meia esquerda', label: 'Meia esquerda' },
  { value: 'meia ofensivo', label: 'Meia ofensivo' },
  { value: 'ponta direita', label: 'Ponta direita' },
  { value: 'ponta esquerda', label: 'Ponta esquerda' },
  { value: 'segundo atacante', label: 'Segundo atacante' },
  { value: 'centroavante', label: 'Centroavante' }
];
const REPORT_SHARE_OPTIONS = Platform.OS === 'ios'
  ? {
      dialogTitle: 'Enviar relatório HUB-PODIUM',
      mimeType: 'application/pdf',
      UTI: 'com.adobe.pdf'
    }
  : {
      dialogTitle: 'Enviar relatório HUB-PODIUM',
      mimeType: 'application/pdf'
    };
const CARD_SHARE_OPTIONS = Platform.OS === 'ios'
  ? {
      dialogTitle: 'Enviar card HUB-PODIUM',
      mimeType: 'image/png',
      UTI: 'public.png'
    }
  : {
      dialogTitle: 'Enviar card HUB-PODIUM',
      mimeType: 'image/png'
    };
const APP_BACKGROUND = require('./assets/hub-podium-app-background.png');

function getCategoryProfile(category) {
  const age = Number(category.replace('sub-', ''));

  if (age <= 12) {
    return {
      type: 'Emocional',
      message: 'Confiança, sonho e apoio da família no centro da devolutiva.',
      focus: 'sonho, autoestima e primeiros passos'
    };
  }

  return {
    type: 'Evolutiva',
    message: 'Performance, gaps e metas para evolução competitiva.',
    focus: 'performance, potencial e evolução'
  };
}

function getVideoAssetName(uri) {
  const filename = uri.split('/').pop() || `hub-podium-video-${Date.now()}.mp4`;
  return filename.includes('.') ? filename : `${filename}.mp4`;
}

function getVideoMimeType(filename) {
  const lowered = filename.toLowerCase();
  if (lowered.endsWith('.mov')) return 'video/quicktime';
  if (lowered.endsWith('.m4v')) return 'video/x-m4v';
  return 'video/mp4';
}

function getPhotoAssetName(uri) {
  const filename = uri.split('/').pop() || `hub-podium-photo-${Date.now()}.jpg`;
  return filename.includes('.') ? filename : `${filename}.jpg`;
}

function getPhotoMimeType(filename) {
  const lowered = filename.toLowerCase();
  if (lowered.endsWith('.png')) return 'image/png';
  if (lowered.endsWith('.webp')) return 'image/webp';
  return 'image/jpeg';
}

function formatFileSize(sizeBytes) {
  return `${(sizeBytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getAssetFileSize(asset) {
  if (typeof asset?.fileSize === 'number' && Number.isFinite(asset.fileSize) && asset.fileSize > 0) {
    return asset.fileSize;
  }

  return null;
}

function normalizeApiBaseUrl(value) {
  return (value || DEFAULT_API_URL).trim().replace(/\/+$/, '') || DEFAULT_API_URL;
}

function isLocalDeviceUrl(value) {
  return /^http:\/\/(localhost|127\.0\.0\.1|192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)/.test(value);
}

function getStartupApiUrl(value) {
  const normalized = normalizeApiBaseUrl(value);
  if (RETIRED_API_URLS.includes(normalized)) return DEFAULT_API_URL;
  return isLocalDeviceUrl(normalized) ? DEFAULT_API_URL : normalized;
}

async function fetchWithTimeout(url, options = {}, timeoutMs = 15000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

function normalizeWhatsAppPhone(value) {
  const digits = String(value || '').replace(/\D/g, '');
  if (!digits) return '';
  return digits.startsWith('55') ? digits : `55${digits}`;
}

function rgbArrayToColor(value, fallback) {
  if (!Array.isArray(value) || value.length < 3) return fallback;
  return `rgb(${value[0]}, ${value[1]}, ${value[2]})`;
}

function getCardTierColors(result) {
  const tier = result?.card_tier || {};
  return {
    accent: rgbArrayToColor(tier.accent_rgb, '#d4af37'),
    secondary: rgbArrayToColor(tier.secondary_rgb, '#8a681d'),
    dark: rgbArrayToColor(tier.dark_rgb, '#111'),
    panel: rgbArrayToColor(tier.panel_rgb, '#1f2937')
  };
}

function buildWhatsAppMessage(result) {
  const match = result?.elite_profile_match;
  const tier = result?.card_tier;
  const track = result?.competition_track === 'feminino' ? 'Feminino' : 'Masculino';
  return [
    `HUB-PODIUM - Análise ${result?.analysis_id || ''}`,
    `Atleta: ${result?.athlete_name || ''}`,
    `Categoria competitiva: ${track}`,
    `Categoria: ${(result?.category || '').toUpperCase()}`,
    `Posição: ${(result?.position || '').toUpperCase()}`,
    `Overall: ${result?.overall || ''}`,
    tier?.label ? `Card: ${tier.label} - ${tier.headline}` : '',
    match?.comparison_text || '',
    `Reconhecimento facial: ${result?.recognition?.video_identity_check || 'pendente'} (${result?.recognition?.match_confidence || 0}%)`,
    'PDF e card disponíveis para compartilhamento pelo app HUB-PODIUM.'
  ].filter(Boolean).join('\n');
}

export default function App() {
  const [apiBaseUrl, setApiBaseUrl] = useState(DEFAULT_API_URL);
  const [athlete, setAthlete] = useState({
    name: '',
    position: '',
    competitionTrack: '',
    responsibleName: '',
    responsibleEmail: '',
    responsibleWhatsapp: '',
    supporterClub: ''
  });
  const [category, setCategory] = useState('sub-12');
  const [photoAsset, setPhotoAsset] = useState(null);
  const [videoAsset, setVideoAsset] = useState(null);
  const [result, setResult] = useState(null);
  const [packageFiles, setPackageFiles] = useState(null);
  const [status, setStatus] = useState('ready');
  const [history, setHistory] = useState([]);
  const [legalConsent, setLegalConsent] = useState({
    privacyAccepted: false,
    termsAccepted: false,
    responsibleAuthorityConfirmed: false,
    contactAccepted: false
  });
  const profile = useMemo(() => getCategoryProfile(category), [category]);
  const cardColors = useMemo(() => getCardTierColors(result), [result]);
  const isBusy = status === 'uploading' || status === 'packaging' || status === 'checking';

  useEffect(() => {
    async function loadState() {
      try {
        const saved = await AsyncStorage.getItem(STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          setApiBaseUrl(getStartupApiUrl(parsed.apiBaseUrl));
          setHistory(parsed.history || []);
        }
      } catch (error) {
        setApiBaseUrl(DEFAULT_API_URL);
      }
    }

    loadState();
  }, []);

  async function persistState(nextHistory = history, nextApiBaseUrl = apiBaseUrl) {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify({
      apiBaseUrl: nextApiBaseUrl,
      history: nextHistory.slice(0, 5)
    }));
  }

  async function openLegalUrl(url) {
    try {
      await Linking.openURL(url);
    } catch (error) {
      Alert.alert('Link indisponível', 'Não foi possível abrir o documento jurídico neste aparelho.');
    }
  }

  function toggleLegalConsent(field) {
    setLegalConsent((current) => ({
      ...current,
      [field]: !current[field]
    }));
  }

  function applySelectedVideo(asset) {
    setVideoAsset(asset);
    setResult(null);
    setPackageFiles(null);
    setStatus('ready');
  }

  async function validateAndApplySelectedVideo(asset) {
    try {
      let detectedSize = getAssetFileSize(asset);

      if (detectedSize == null) {
        const info = await FileSystem.getInfoAsync(asset.uri);
        if (info.exists && typeof info.size === 'number' && Number.isFinite(info.size) && info.size > 0) {
          detectedSize = info.size;
        }
      }

      if (typeof detectedSize === 'number') {
        asset = {
          ...asset,
          fileSize: detectedSize
        };
      }

      if (typeof detectedSize === 'number' && detectedSize > MAX_VIDEO_UPLOAD_BYTES) {
        Alert.alert(
          'Vídeo acima da faixa recomendada',
          `O vídeo selecionado tem ${formatFileSize(detectedSize)}. O envio continuará liberado para teste beta, mas arquivos muito grandes podem falhar por rede, memória do aparelho ou tempo de upload.`
        );
      }
    } catch (error) {
      // Se o tamanho não puder ser lido, seguimos com o fluxo normal.
    }

    applySelectedVideo(asset);
  }

  function applySelectedPhoto(asset) {
    setPhotoAsset({
      uri: asset.uri,
      base64: asset.base64,
      fileName: asset.fileName || getPhotoAssetName(asset.uri),
      mimeType: asset.mimeType || getPhotoMimeType(asset.fileName || asset.uri)
    });
    setResult(null);
    setPackageFiles(null);
    setStatus('ready');
  }

  async function ensureCameraPermission() {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Câmera necessária', 'Permita acesso à câmera para capturar foto e vídeo do atleta.');
      return false;
    }
    return true;
  }

  async function pickVideo() {
    const selected = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      quality: 1
    });

    if (!selected.canceled) {
      await validateAndApplySelectedVideo(selected.assets[0]);
    }
  }

  async function recordVideo() {
    const allowed = await ensureCameraPermission();
    if (!allowed) return;

    const selected = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      quality: Platform.OS === 'android' ? 0.6 : 0.8,
      videoMaxDuration: 60
    });

    if (!selected.canceled) {
      await validateAndApplySelectedVideo(selected.assets[0]);
    }
  }

  async function pickPhoto() {
    const selected = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [3, 4],
      quality: 1,
      base64: true
    });

    if (!selected.canceled) {
      applySelectedPhoto(selected.assets[0]);
    }
  }

  async function takePhoto() {
    const allowed = await ensureCameraPermission();
    if (!allowed) return;

    const selected = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [3, 4],
      quality: 1,
      base64: true
    });

    if (!selected.canceled) {
      applySelectedPhoto(selected.assets[0]);
    }
  }

  async function runBetaAnalysis() {
    if (!athlete.name || !athlete.position || !athlete.competitionTrack || !athlete.responsibleName || !photoAsset || !videoAsset?.uri) {
      Alert.alert('Atenção', 'Preencha atleta, responsável, masculino/feminino, posição, foto do atleta e selecione um vídeo.');
      return;
    }

    if (!legalConsent.privacyAccepted || !legalConsent.termsAccepted || !legalConsent.responsibleAuthorityConfirmed) {
      Alert.alert(
        'Consentimento obrigatório',
        'Confirme a política de privacidade, os termos de uso e a responsabilidade legal pelo envio dos dados antes de continuar.'
      );
      return;
    }

    setStatus('uploading');
    setPackageFiles(null);

    try {
      const activeApiUrl = normalizeApiBaseUrl(apiBaseUrl);
      const filename = getVideoAssetName(videoAsset.uri);
      const photoFilename = photoAsset.fileName || getPhotoAssetName(photoAsset.uri);
      const photoMimeType = photoAsset.mimeType || getPhotoMimeType(photoFilename);
      const formData = new FormData();
      formData.append('video', {
        uri: videoAsset.uri,
        name: filename,
        type: getVideoMimeType(filename)
      });
      formData.append('athlete_photo', {
        uri: photoAsset.uri,
        name: photoFilename,
        type: photoMimeType
      });
      formData.append('athlete_name', athlete.name);
      formData.append('category', category);
      formData.append('position', athlete.position);
      formData.append('competition_track', athlete.competitionTrack);
      formData.append('responsible_name', athlete.responsibleName);
      formData.append('responsible_email', athlete.responsibleEmail || '');
      formData.append('responsible_whatsapp', athlete.responsibleWhatsapp || '');
      formData.append('supporter_club', athlete.supporterClub || '');
      formData.append('privacy_accepted', legalConsent.privacyAccepted ? 'true' : 'false');
      formData.append('terms_accepted', legalConsent.termsAccepted ? 'true' : 'false');
      formData.append('responsible_authority_confirmed', legalConsent.responsibleAuthorityConfirmed ? 'true' : 'false');
      formData.append('contact_accepted', legalConsent.contactAccepted ? 'true' : 'false');
      formData.append('filename', filename);
      formData.append('video_client_size_bytes', String(videoAsset.fileSize || ''));
      formData.append('athlete_photo_filename', photoFilename);
      formData.append('athlete_photo_mime_type', photoMimeType);

      const response = await fetchWithTimeout(`${activeApiUrl}/beta/analyze-video`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'X-HUB-PODIUM-BUILD': APP_BUILD_LABEL
        },
        body: formData
      }, 10 * 60 * 1000);
      const responseBody = await response.text();

      if (!response.ok) {
        let apiError = `API ${response.status}`;
        try {
          const payload = JSON.parse(responseBody);
          if (response.status === 413) {
            apiError = payload?.message || 'O servidor rejeitou o upload antes da análise. Vamos revisar o tamanho real do arquivo e a conexão deste aparelho.';
          } else if (payload?.error) {
            apiError = payload.error;
          }
        } catch (error) {
          if (response.status === 413) {
            apiError = 'O servidor rejeitou o upload antes da análise. Vamos revisar o tamanho real do arquivo e a conexão deste aparelho.';
          } else if (responseBody) {
            apiError = responseBody.slice(0, 180);
          }
        }
        throw new Error(apiError);
      }

      const analysis = JSON.parse(responseBody);
      setResult(analysis);
      setStatus('analyzed');

      const nextHistory = [
        {
          analysisId: analysis.analysis_id,
          athleteName: analysis.athlete_name,
          category: analysis.category,
          competitionTrack: analysis.competition_track,
          overall: analysis.overall
        },
        ...history
      ].slice(0, 5);
      setHistory(nextHistory);
      await persistState(nextHistory, activeApiUrl);
    } catch (error) {
      setStatus('error');
      Alert.alert('Erro na beta', `Não foi possível conectar o app ao backend.\n\nDetalhe: ${error.message}`);
    }
  }

  async function saveBase64File(filename, base64) {
    const fileUri = `${FileSystem.documentDirectory}${filename}`;
    await FileSystem.writeAsStringAsync(fileUri, base64, {
      encoding: FileSystem.EncodingType.Base64
    });
    return fileUri;
  }

  async function generatePackage() {
    if (!result) return;

    setStatus('packaging');

    try {
      const activeApiUrl = normalizeApiBaseUrl(apiBaseUrl);
      const response = await fetchWithTimeout(`${activeApiUrl}/beta/generate-package`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result)
      });

      if (!response.ok) {
        throw new Error(`API ${response.status}`);
      }

      const payload = await response.json();
      const reportUri = await saveBase64File(payload.report.filename, payload.report.base64);
      const cardUri = await saveBase64File(payload.card.filename, payload.card.base64);

      setPackageFiles({
        reportUri,
        cardUri,
        reportFilename: payload.report.filename,
        cardFilename: payload.card.filename
      });
      setStatus('packaged');
    } catch (error) {
      setStatus('error');
      Alert.alert('Erro no pacote', 'Não foi possível gerar PDF e card.');
    }
  }

  async function shareFile(uri, options = {}) {
    const available = await Sharing.isAvailableAsync();
    if (!available) {
      Alert.alert('Compartilhamento indisponivel', uri);
      return;
    }
    await Sharing.shareAsync(uri, options);
  }

  async function shareReportOnWhatsApp() {
    if (!packageFiles?.reportUri) {
      Alert.alert('Relatório pendente', 'Gere o PDF e o card antes de enviar o relatório.');
      return;
    }

    await shareFile(packageFiles.reportUri, REPORT_SHARE_OPTIONS);
  }

  async function shareCardOnWhatsApp() {
    if (!packageFiles?.cardUri) {
      Alert.alert('Card pendente', 'Gere o PDF e card antes de enviar o card.');
      return;
    }

    await shareFile(packageFiles.cardUri, CARD_SHARE_OPTIONS);
  }

  async function shareResultOnWhatsApp() {
    if (!result) return;

    const phone = normalizeWhatsAppPhone(athlete.responsibleWhatsapp || result.responsible_whatsapp);
    if (!phone) {
      Alert.alert('WhatsApp obrigatório', 'Informe o WhatsApp do responsável para enviar o resumo.');
      return;
    }

    const text = encodeURIComponent(buildWhatsAppMessage(result));
    const appUrl = `whatsapp://send?phone=${phone}&text=${text}`;
    const webUrl = `https://wa.me/${phone}?text=${text}`;

    try {
      const canOpenApp = await Linking.canOpenURL(appUrl);
      await Linking.openURL(canOpenApp ? appUrl : webUrl);
    } catch (error) {
      Alert.alert('WhatsApp indisponível', 'Não foi possível abrir o WhatsApp neste aparelho.');
    }
  }

  async function updateApiBaseUrl(value) {
    setApiBaseUrl(value);
    await persistState(history, value);
  }

  async function resetApiBaseUrl() {
    setApiBaseUrl(DEFAULT_API_URL);
    await persistState(history, DEFAULT_API_URL);
  }

  async function testApiConnection() {
    const activeApiUrl = normalizeApiBaseUrl(apiBaseUrl);
    setStatus('checking');

    try {
      const response = await fetchWithTimeout(`${activeApiUrl}/health`);
      if (!response.ok) {
        throw new Error(`API ${response.status}`);
      }
      Alert.alert('Conexão OK', 'Backend HUB-PODIUM ativo.');
      setStatus('ready');
      await persistState(history, activeApiUrl);
    } catch (error) {
      setStatus('error');
      Alert.alert('Erro de conexão', `Backend indisponível.\n\nDetalhe: ${error.message}`);
    }
  }

  return (
    <ImageBackground source={APP_BACKGROUND} style={styles.background} imageStyle={styles.backgroundImage}>
      <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.content}>
          <View style={styles.header}>
            <Text style={styles.brand}>HUB-PODIUM</Text>
            <Text style={styles.title}>Beta HUB-ELITE</Text>
            <Text style={styles.subtitle}>Análise automatizada por vídeo para Sub-8 a Sub-20 em iPhone e Android</Text>
          </View>

          <View style={styles.panel}>
          <Text style={styles.panelTitle}>Conexao</Text>
          <TextInput
            style={styles.input}
            placeholder="URL da API"
            value={apiBaseUrl}
            autoCapitalize="none"
            onChangeText={updateApiBaseUrl}
          />
          <View style={styles.connectionActions}>
            <Pressable style={styles.connectionButton} onPress={resetApiBaseUrl} disabled={isBusy}>
              <Text style={styles.connectionButtonText}>API beta</Text>
            </Pressable>
            <Pressable style={styles.connectionButton} onPress={testApiConnection} disabled={isBusy}>
              <Text style={styles.connectionButtonText}>Testar API</Text>
            </Pressable>
          </View>
          </View>

          <View style={styles.panel}>
          <Text style={styles.panelTitle}>Atleta</Text>
          <TextInput
            style={styles.input}
            placeholder="Nome do atleta"
            value={athlete.name}
            onChangeText={(value) => setAthlete({ ...athlete, name: value })}
          />
          <TextInput
            style={styles.input}
            placeholder="Nome do responsável"
            value={athlete.responsibleName}
            onChangeText={(value) => setAthlete({ ...athlete, responsibleName: value })}
          />
          <TextInput
            style={styles.input}
            placeholder="E-mail do responsável"
            value={athlete.responsibleEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            onChangeText={(value) => setAthlete({ ...athlete, responsibleEmail: value })}
          />
          <TextInput
            style={styles.input}
            placeholder="WhatsApp do responsável"
            value={athlete.responsibleWhatsapp}
            keyboardType="phone-pad"
            onChangeText={(value) => setAthlete({ ...athlete, responsibleWhatsapp: value })}
          />
          <TextInput
            style={styles.input}
            placeholder="Clube do coração"
            value={athlete.supporterClub}
            onChangeText={(value) => setAthlete({ ...athlete, supporterClub: value })}
          />
          <Text style={styles.label}>Posição</Text>
          <View style={styles.positionGrid}>
            {POSITION_OPTIONS.map((item) => {
              const selected = athlete.position === item.value;
              return (
                <Pressable
                  key={item.value}
                  style={[styles.positionOption, selected && styles.positionOptionSelected]}
                  onPress={() => {
                    setAthlete({ ...athlete, position: item.value });
                    setResult(null);
                    setPackageFiles(null);
                  }}
                  disabled={isBusy}
                >
                  <Text style={[styles.positionOptionText, selected && styles.positionOptionTextSelected]}>{item.label}</Text>
                </Pressable>
              );
            })}
          </View>

          <Text style={styles.label}>Masculino ou feminino</Text>
          <View style={styles.trackSelector}>
            {COMPETITION_TRACK_OPTIONS.map((item) => {
              const selected = athlete.competitionTrack === item.value;
              return (
                <Pressable
                  key={item.value}
                  style={[styles.trackOption, selected && styles.trackOptionSelected]}
                  onPress={() => {
                    setAthlete({ ...athlete, competitionTrack: item.value });
                    setResult(null);
                    setPackageFiles(null);
                  }}
                  disabled={isBusy}
                >
                  <Text style={[styles.trackOptionText, selected && styles.trackOptionTextSelected]}>{item.label}</Text>
                </Pressable>
              );
            })}
          </View>

          <View style={styles.photoRow}>
            <View style={styles.photoActions}>
              <Pressable style={styles.photoButton} onPress={takePhoto} disabled={isBusy}>
                <Text style={styles.secondaryButtonText}>{photoAsset ? 'Nova foto' : 'Tirar foto'}</Text>
              </Pressable>
              <Pressable style={styles.photoButton} onPress={pickPhoto} disabled={isBusy}>
                <Text style={styles.secondaryButtonText}>Galeria</Text>
              </Pressable>
            </View>
            <View style={styles.photoPreview}>
              {photoAsset ? (
                <>
                  <Image source={{ uri: photoAsset.uri }} style={styles.photoImage} />
                  <View pointerEvents="none" style={styles.photoGuideOverlay}>
                    <View style={styles.photoGuideHead} />
                    <View style={styles.photoGuideShoulders} />
                  </View>
                </>
              ) : (
                <View style={styles.photoGuideEmpty}>
                  <View style={styles.photoGuideHead} />
                  <View style={styles.photoGuideShoulders} />
                  <Text style={styles.photoPlaceholder}>Rosto e ombros</Text>
                </View>
              )}
            </View>
          </View>
          <Text style={styles.photoHint}>Foto obrigatória para referência visual do atleta no vídeo.</Text>
          <View style={styles.photoGuideBox}>
            <Text style={styles.photoGuideTitle}>Padrão da foto do card</Text>
            {PHOTO_GUIDE_POINTS.map((item) => (
              <View key={item} style={styles.photoGuidePointRow}>
                <View style={styles.photoGuideDot} />
                <Text style={styles.photoGuidePointText}>{item}</Text>
              </View>
            ))}
          </View>

          <Text style={styles.label}>Categoria</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categoryScroller}>
            {CATEGORY_OPTIONS.map((item) => {
              const selected = item === category;
              return (
                <Pressable
                  key={item}
                  style={[styles.categoryChip, selected && styles.categoryChipSelected]}
                  onPress={() => {
                    setCategory(item);
                    setResult(null);
                    setPackageFiles(null);
                  }}
                >
                  <Text style={[styles.categoryText, selected && styles.categoryTextSelected]}>{item.toUpperCase()}</Text>
                </Pressable>
              );
            })}
          </ScrollView>

          <View style={styles.profileBox}>
            <Text style={styles.profileType}>{profile.type}</Text>
            <Text style={styles.profileMessage}>{profile.message}</Text>
            <Text style={styles.profileFocus}>{profile.focus}</Text>
          </View>
          <View style={styles.legalBox}>
            <Text style={styles.legalTitle}>Base jurídica do envio</Text>
            <Text style={styles.legalDescription}>
              Antes da análise, confirme os documentos jurídicos e a legitimidade do envio do material do atleta.
            </Text>
            <Pressable style={styles.legalLinkRow} onPress={() => openLegalUrl(PRIVACY_URL)} disabled={isBusy}>
              <Text style={styles.legalLinkText}>Ler política de privacidade</Text>
            </Pressable>
            <Pressable style={styles.legalLinkRow} onPress={() => openLegalUrl(TERMS_URL)} disabled={isBusy}>
              <Text style={styles.legalLinkText}>Ler termos de uso</Text>
            </Pressable>
            <Pressable style={styles.checkboxRow} onPress={() => toggleLegalConsent('privacyAccepted')} disabled={isBusy}>
              <View style={[styles.checkbox, legalConsent.privacyAccepted && styles.checkboxChecked]}>
                {legalConsent.privacyAccepted ? <Text style={styles.checkboxCheck}>✓</Text> : null}
              </View>
              <Text style={styles.checkboxText}>Declaro que li e compreendi a política de privacidade.</Text>
            </Pressable>
            <Pressable style={styles.checkboxRow} onPress={() => toggleLegalConsent('termsAccepted')} disabled={isBusy}>
              <View style={[styles.checkbox, legalConsent.termsAccepted && styles.checkboxChecked]}>
                {legalConsent.termsAccepted ? <Text style={styles.checkboxCheck}>✓</Text> : null}
              </View>
              <Text style={styles.checkboxText}>Declaro que li e compreendi os termos de uso da HUB-PODIUM.</Text>
            </Pressable>
            <Pressable style={styles.checkboxRow} onPress={() => toggleLegalConsent('responsibleAuthorityConfirmed')} disabled={isBusy}>
              <View style={[styles.checkbox, legalConsent.responsibleAuthorityConfirmed && styles.checkboxChecked]}>
                {legalConsent.responsibleAuthorityConfirmed ? <Text style={styles.checkboxCheck}>✓</Text> : null}
              </View>
              <Text style={styles.checkboxText}>Confirmo que sou o responsável legal ou tenho autorização válida para enviar os dados, a foto e o vídeo do atleta.</Text>
            </Pressable>
            <Pressable style={styles.checkboxRow} onPress={() => toggleLegalConsent('contactAccepted')} disabled={isBusy}>
              <View style={[styles.checkbox, legalConsent.contactAccepted && styles.checkboxChecked]}>
                {legalConsent.contactAccepted ? <Text style={styles.checkboxCheck}>✓</Text> : null}
              </View>
              <Text style={styles.checkboxText}>Autorizo contato operacional da HUB-PODIUM sobre esta análise e sua devolutiva.</Text>
            </Pressable>
          </View>
          </View>

          <View style={styles.actions}>
          <View style={styles.videoHintBox}>
            <Text style={styles.videoHintTitle}>Qualidade do vídeo</Text>
            <Text style={styles.videoHintText}>Envie vídeos em alta resolução, com boa iluminação e enquadramento claro para melhorar a análise do atleta.</Text>
            <Text style={styles.videoHintMeta}>Beta atual sem bloqueio rígido de tamanho. Vídeos muito grandes podem falhar por rede ou tempo de envio.</Text>
            <Text style={styles.videoHintMeta}>Build ativa: {APP_BUILD_LABEL}</Text>
          </View>
          <Pressable style={styles.secondaryButton} onPress={recordVideo} disabled={isBusy}>
            <Text style={styles.secondaryButtonText}>{videoAsset ? 'Gravar novo vídeo' : 'Gravar vídeo com c?mera'}</Text>
          </Pressable>
          <Pressable style={styles.secondaryButton} onPress={pickVideo} disabled={isBusy}>
            <Text style={styles.secondaryButtonText}>{videoAsset ? 'Trocar por vídeo da galeria' : 'Selecionar vídeo da galeria'}</Text>
          </Pressable>
          {videoAsset ? (
            <View style={styles.videoMetaBox}>
              <Text style={styles.videoMetaText}>Vídeo selecionado: {videoAsset.fileName || getVideoAssetName(videoAsset.uri)}</Text>
              <Text style={styles.videoMetaText}>Tamanho detectado: {typeof videoAsset.fileSize === 'number' ? formatFileSize(videoAsset.fileSize) : 'não informado pelo aparelho'}</Text>
            </View>
          ) : null}
          <Pressable style={[styles.primaryButton, isBusy && styles.disabledButton]} onPress={runBetaAnalysis} disabled={isBusy}>
            {status === 'uploading' ? <ActivityIndicator color="#111" /> : <Text style={styles.primaryButtonText}>Analisar vídeo</Text>}
          </Pressable>
          </View>

          {result && (
            <View style={[styles.resultPanel, { backgroundColor: cardColors.dark, borderColor: cardColors.accent }]}>
            <View style={[styles.tierStripe, { backgroundColor: cardColors.accent }]} />
            <View style={styles.cardHeader}>
              <View>
                <Text style={styles.cardName}>{result.athlete_name}</Text>
                <Text style={[styles.cardMeta, { color: cardColors.accent }]}>
                  {result.category.toUpperCase()} | {result.position.toUpperCase()} | {(result.competition_track || athlete.competitionTrack).toUpperCase()}
                </Text>
                {result.card_tier?.label ? (
                  <Text style={[styles.cardTier, { color: cardColors.accent }]}>{result.card_tier.label} | {result.card_tier.headline}</Text>
                ) : null}
              </View>
              <Text style={[styles.overall, { color: cardColors.accent }]}>{result.overall}</Text>
            </View>

            <View style={styles.statsGrid}>
              <Text style={[styles.stat, { color: cardColors.accent }]}>VEL {result.speed}</Text>
              <Text style={[styles.stat, { color: cardColors.accent }]}>TEC {result.technique}</Text>
              <Text style={[styles.stat, { color: cardColors.accent }]}>QI {result.game_iq}</Text>
              <Text style={[styles.stat, { color: cardColors.accent }]}>FIS {result.physical}</Text>
              <Text style={[styles.stat, { color: cardColors.accent }]}>POT {result.potential}</Text>
            </View>

            <View style={[styles.deliveryBox, { borderColor: cardColors.accent }]}>
              <Text style={[styles.deliveryTitle, { color: cardColors.dark }]}>HUB-ELITE</Text>
              <Text style={styles.deliverySectionTitle}>Leitura de perfil</Text>
              <Text style={styles.deliveryText}>{result.executive_summary?.profile_reading || result.elite_profile_match?.comparison_text}</Text>
              <Text style={styles.deliverySectionTitle}>Direção evolutiva</Text>
              <Text style={styles.deliveryText}>{result.executive_summary?.development_recommendation || result.elite_profile_match?.development_note}</Text>
              <Text style={styles.deliveryText}>{result.executive_summary?.category_guidance || result.category_profile.message}</Text>
              <Text style={styles.deliverySectionTitle}>Calibração HUB-ELITE</Text>
              <Text style={styles.deliveryText}>Consistência posicional: {result.calibration?.position_consistency?.score || 0} | {String(result.calibration?.position_consistency?.band || '').replace('_', ' ')}</Text>
              <Text style={styles.deliveryText}>Coerência funcional: {result.calibration?.functional_family_coherence?.score || 0} | slot {String(result.calibration?.functional_family_coherence?.canonical_position_code || '').replace('_', ' ')}</Text>
              <Text style={styles.deliveryText}>Similaridade refinada: {result.calibration?.similarity_refinement?.overall_score || result.elite_profile_match?.similarity_score || 0}%</Text>
              <Text style={styles.deliveryText}>Encaixe de estilo: {(result.calibration?.similarity_refinement?.shared_style_tags || []).join(', ') || 'sem destaque dominante ainda'}</Text>
              <Text style={styles.deliveryText}>Fase competitiva: {String(result.calibration?.category_gap_matrix?.category_stage || '').replace('_', ' ')}</Text>
              <Text style={styles.deliveryText}>{result.calibration?.category_gap_matrix?.summary || result.executive_summary?.category_gap_summary}</Text>
              <Text style={styles.deliverySectionTitle}>Leitura para pais e clubes</Text>
              <Text style={styles.deliveryText}>{result.calibration?.comparative_explainability?.parent_summary || result.executive_summary?.parent_explanation}</Text>
              <Text style={styles.deliveryText}>{result.calibration?.comparative_explainability?.club_summary || result.executive_summary?.club_explanation}</Text>
              {(result.calibration?.development_gaps?.top_priorities || []).slice(0, 3).map((item) => (
                <Text key={item.metric} style={styles.deliveryText}>
                  Gap {item.label}: {item.gap} | foco em {item.focus}
                </Text>
              ))}
              <Text style={styles.deliverySectionTitle}>Mapa Golden Ball</Text>
              <Text style={styles.deliveryText}>Estágio atual: {result.calibration?.golden_ball_map?.current_stage || 'Fundação competitiva'}</Text>
              <Text style={styles.deliveryText}>Próximo est?gio: {result.calibration?.golden_ball_map?.next_stage || 'n/a'}</Text>
              <Text style={styles.deliveryText}>Stage score: {result.calibration?.golden_ball_map?.stage_score || 0}</Text>
              <Text style={styles.deliveryText}>Próximo checkpoint: {result.calibration?.golden_ball_map?.next_cycle_checkpoint?.label || 'checkpoint maximo do ciclo atingido'}</Text>
              <Text style={styles.deliverySectionTitle}>Roadmap de treino</Text>
              <Text style={styles.deliveryText}>{result.calibration?.training_roadmap?.summary || result.executive_summary?.training_roadmap_summary}</Text>
              {(result.calibration?.training_roadmap?.cycles || []).slice(0, 3).map((cycle) => (
                <View key={cycle.cycle} style={styles.trainingCycleBox}>
                  <Text style={styles.trainingCycleTitle}>{String(cycle.cycle || '').replace('_', ' ').toUpperCase()} | {String(cycle.label || '').toUpperCase()}</Text>
                  <Text style={styles.deliveryText}>{cycle.goal}</Text>
                  <Text style={styles.deliveryText}>Blocos: {(cycle.training_blocks || []).join(', ')}</Text>
                  <Text style={styles.deliveryText}>{cycle.checkpoint}</Text>
                </View>
              ))}
              <Text style={styles.deliverySectionTitle}>HUB-PODIUM Evolução</Text>
              <Text style={styles.deliveryText}>Plano: {result.calibration?.evolution_subscription?.plan_name || 'HUB-PODIUM Evolução'}</Text>
              <Text style={styles.deliveryText}>Módulo: {result.calibration?.evolution_subscription?.module_name || 'Módulo evolutivo'}</Text>
              <Text style={styles.deliveryText}>Faixa: {result.calibration?.evolution_subscription?.program_tier || 'Desenvolvimento competitivo'}</Text>
              <Text style={styles.deliveryText}>{result.calibration?.evolution_subscription?.sales_summary || result.executive_summary?.subscription_summary}</Text>
              <Text style={styles.deliverySectionTitle}>Oferta comercial</Text>
              <Text style={styles.deliveryText}>{result.calibration?.customer_offers?.summary || result.executive_summary?.customer_offer_summary}</Text>
              <Text style={styles.deliveryText}>Pais: {result.calibration?.customer_offers?.parent_offer?.headline || ''}</Text>
              <Text style={styles.deliveryText}>Clubes: {result.calibration?.customer_offers?.club_offer?.headline || ''}</Text>
              <Text style={styles.deliveryText}>Escolas: {result.calibration?.customer_offers?.school_offer?.headline || ''}</Text>
              <Text style={styles.deliverySectionTitle}>Onboarding</Text>
              <Text style={styles.deliveryText}>{result.calibration?.onboarding_journey?.summary || result.executive_summary?.onboarding_summary}</Text>
              {(result.calibration?.onboarding_journey?.steps || []).map((step) => (
                <View key={step.step} style={styles.trainingCycleBox}>
                  <Text style={styles.trainingCycleTitle}>ETAPA {step.step} | {String(step.title || '').toUpperCase()}</Text>
                  <Text style={styles.deliveryText}>{step.description}</Text>
                </View>
              ))}
              <Text style={styles.deliverySectionTitle}>Planos comerciais</Text>
              <Text style={styles.deliveryText}>{result.calibration?.commercial_plans?.summary || result.executive_summary?.commercial_plan_summary}</Text>
              {(result.calibration?.commercial_plans?.launch_order || []).map((key) => {
                const plan = result.calibration?.commercial_plans?.plans?.[key];
                if (!plan) return null;
                return (
                  <View key={key} style={styles.trainingCycleBox}>
                    <Text style={styles.trainingCycleTitle}>{String(plan.plan_name || '').toUpperCase()}</Text>
                    <Text style={styles.deliveryText}>Preco: R$ {Number(plan.price_brl_month || 0).toFixed(2)} | {plan.billing_cycle}</Text>
                    <Text style={styles.deliveryText}>Canal: {plan.primary_channel}</Text>
                    <Text style={styles.deliveryText}>{plan.short_site_copy}</Text>
                    <Text style={styles.deliveryText}>LinkedIn: {plan.short_linkedin_copy}</Text>
                    <Text style={styles.deliveryText}>WhatsApp: {plan.short_whatsapp_copy}</Text>
                  </View>
                );
              })}
              <Text style={styles.deliverySectionTitle}>Fluxo de ativacao</Text>
              <Text style={styles.deliveryText}>{result.calibration?.sales_activation_flow?.summary || result.executive_summary?.sales_activation_summary}</Text>
              {(result.calibration?.sales_activation_flow?.activation_steps || []).map((step) => (
                <View key={`${step.step}-${step.segment}`} style={styles.trainingCycleBox}>
                  <Text style={styles.trainingCycleTitle}>ETAPA {step.step} | {String(step.plan_name || '').toUpperCase()}</Text>
                  <Text style={styles.deliveryText}>{step.conversion_goal}</Text>
                  <Text style={styles.deliveryText}>Canal principal: {step.entry_channel}</Text>
                  <Text style={styles.deliveryText}>Site: {step.message_asset?.site}</Text>
                  <Text style={styles.deliveryText}>LinkedIn: {step.message_asset?.linkedin}</Text>
                  <Text style={styles.deliveryText}>WhatsApp: {step.message_asset?.whatsapp}</Text>
                </View>
              ))}
              <Text style={styles.deliveryText}>Trilha: {(result.competition_track || athlete.competitionTrack || '').toUpperCase()}</Text>
              <Text style={styles.deliveryText}>Reconhecimento facial: {result.recognition?.video_identity_check} | {result.recognition?.match_confidence || 0}%</Text>
              <Text style={styles.deliveryText}>Clube do coração: {result.supporter_club || athlete.supporterClub || 'Não informado'}</Text>
              <Text style={styles.deliveryNote}>{result.executive_summary?.institutional_note || result.elite_profile_match?.disclaimer}</Text>
              <Text style={styles.deliveryText}>Análise ID: {result.analysis_id}</Text>
            </View>

            <Pressable style={styles.secondaryButtonDark} onPress={shareResultOnWhatsApp}>
              <Text style={styles.secondaryButtonDarkText}>Enviar resumo no WhatsApp</Text>
            </Pressable>
            <Pressable style={styles.primaryButton} onPress={generatePackage} disabled={status === 'packaging'}>
              {status === 'packaging' ? <ActivityIndicator color="#111" /> : <Text style={styles.primaryButtonText}>Gerar PDF e card</Text>}
            </Pressable>
            </View>
          )}

          {packageFiles && (
            <View style={styles.panel}>
            <Text style={styles.panelTitle}>Entregaveis</Text>
            <Pressable style={styles.secondaryButton} onPress={shareReportOnWhatsApp}>
              <Text style={styles.secondaryButtonText}>Enviar relatório no WhatsApp</Text>
            </Pressable>
            <Pressable style={styles.secondaryButton} onPress={shareCardOnWhatsApp}>
              <Text style={styles.secondaryButtonText}>Enviar card no WhatsApp</Text>
            </Pressable>
            <Pressable style={styles.secondaryButton} onPress={() => shareFile(packageFiles.reportUri, REPORT_SHARE_OPTIONS)}>
              <Text style={styles.secondaryButtonText}>Compartilhar PDF</Text>
            </Pressable>
            <Pressable style={styles.secondaryButton} onPress={() => shareFile(packageFiles.cardUri, CARD_SHARE_OPTIONS)}>
              <Text style={styles.secondaryButtonText}>Compartilhar card</Text>
            </Pressable>
            </View>
          )}

          {history.length > 0 && (
            <View style={styles.panel}>
            <Text style={styles.panelTitle}>Historico beta</Text>
            {history.map((item) => (
              <View key={item.analysisId} style={styles.historyRow}>
                <Text style={styles.historyName}>{item.athleteName}</Text>
                <Text style={styles.historyMeta}>{item.category.toUpperCase()} | {(item.competitionTrack || '').toUpperCase()} | OVR {item.overall}</Text>
              </View>
            ))}
            </View>
          )}
        </ScrollView>
      </SafeAreaView>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: { flex: 1, backgroundColor: '#020408' },
  backgroundImage: { resizeMode: 'cover' },
  container: { flex: 1, backgroundColor: 'rgba(4, 6, 10, 0.56)' },
  content: { padding: 20, paddingBottom: 42 },
  header: { paddingTop: 24, paddingBottom: 20, paddingHorizontal: 16, borderRadius: 8, borderWidth: 1, borderColor: 'rgba(212, 175, 55, 0.38)', backgroundColor: 'rgba(0, 0, 0, 0.42)', marginBottom: 14 },
  brand: { color: '#d4af37', fontWeight: '900', letterSpacing: 1, marginBottom: 8 },
  title: { color: '#f8fafc', fontSize: 34, fontWeight: '900' },
  subtitle: { color: '#e5e7eb', fontSize: 16, marginTop: 6, lineHeight: 22 },
  panel: { backgroundColor: 'rgba(255, 255, 255, 0.95)', borderRadius: 8, padding: 16, borderWidth: 1, borderColor: 'rgba(212, 175, 55, 0.22)', marginBottom: 14 },
  panelTitle: { fontSize: 18, fontWeight: '900', marginBottom: 14, color: '#111' },
  input: { backgroundColor: '#f9fafb', padding: 14, marginBottom: 12, borderRadius: 8, borderWidth: 1, borderColor: '#d1d5db' },
  connectionActions: { flexDirection: 'row', gap: 10 },
  connectionButton: { flex: 1, minHeight: 44, borderRadius: 8, borderWidth: 1, borderColor: '#111', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fff' },
  connectionButtonText: { color: '#111', fontWeight: '900' },
  photoRow: { flexDirection: 'row', alignItems: 'stretch', marginBottom: 8 },
  photoActions: { flex: 1, marginRight: 12 },
  photoButton: { minHeight: 44, borderRadius: 8, borderWidth: 1, borderColor: '#111', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fff', marginBottom: 8 },
  photoPreview: { width: 92, height: 122, borderRadius: 8, borderWidth: 1, borderColor: '#d1d5db', overflow: 'hidden', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f9fafb', position: 'relative' },
  photoImage: { width: '100%', height: '100%' },
  photoPlaceholder: { color: '#64748b', fontWeight: '900' },
  photoHint: { color: '#64748b', fontSize: 12, lineHeight: 16, marginBottom: 12 },
  photoGuideBox: { backgroundColor: '#f8fafc', borderRadius: 8, borderWidth: 1, borderColor: '#dbe4ee', padding: 12, marginBottom: 14 },
  photoGuideTitle: { color: '#0f172a', fontWeight: '900', marginBottom: 8 },
  photoGuidePointRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 6 },
  photoGuideDot: { width: 7, height: 7, borderRadius: 999, backgroundColor: '#d4af37', marginRight: 8 },
  photoGuidePointText: { color: '#475569', fontSize: 13, lineHeight: 18, flex: 1 },
  photoGuideOverlay: { ...StyleSheet.absoluteFillObject, alignItems: 'center', justifyContent: 'center', paddingTop: 10 },
  photoGuideEmpty: { flex: 1, width: '100%', alignItems: 'center', justifyContent: 'center', paddingTop: 10 },
  photoGuideHead: { width: 28, height: 28, borderRadius: 999, borderWidth: 1.5, borderColor: 'rgba(212, 175, 55, 0.88)', backgroundColor: 'rgba(212, 175, 55, 0.14)' },
  photoGuideShoulders: { width: 56, height: 30, borderWidth: 1.5, borderColor: 'rgba(212, 175, 55, 0.88)', borderTopWidth: 0, borderBottomLeftRadius: 18, borderBottomRightRadius: 18, marginTop: 6, backgroundColor: 'rgba(212, 175, 55, 0.08)' },
  label: { fontWeight: '800', color: '#111', marginBottom: 8 },
  positionGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 12 },
  positionOption: { width: '48.5%', minHeight: 48, alignItems: 'center', justifyContent: 'center', borderRadius: 8, borderWidth: 1, borderColor: '#cbd5e1', backgroundColor: '#fff', marginBottom: 10, paddingHorizontal: 10, paddingVertical: 8 },
  positionOptionSelected: { backgroundColor: '#111', borderColor: '#111' },
  positionOptionText: { color: '#111', fontWeight: '800', textAlign: 'center' },
  positionOptionTextSelected: { color: '#d4af37' },
  trackSelector: { flexDirection: 'row', gap: 10, marginBottom: 12 },
  trackOption: { flex: 1, minHeight: 46, alignItems: 'center', justifyContent: 'center', borderRadius: 8, borderWidth: 1, borderColor: '#cbd5e1', backgroundColor: '#fff' },
  trackOptionSelected: { backgroundColor: '#111', borderColor: '#111' },
  trackOptionText: { color: '#111', fontWeight: '900' },
  trackOptionTextSelected: { color: '#d4af37' },
  categoryScroller: { marginBottom: 14 },
  categoryChip: { height: 42, minWidth: 72, alignItems: 'center', justifyContent: 'center', marginRight: 8, borderRadius: 8, borderWidth: 1, borderColor: '#cbd5e1', backgroundColor: '#fff' },
  categoryChipSelected: { backgroundColor: '#111', borderColor: '#111' },
  categoryText: { color: '#111', fontWeight: '800' },
  categoryTextSelected: { color: '#d4af37' },
  profileBox: { backgroundColor: '#edf6ff', borderRadius: 8, padding: 12, borderWidth: 1, borderColor: '#bfdbfe' },
  profileType: { color: '#0f3f6e', fontWeight: '900', marginBottom: 4 },
  profileMessage: { color: '#1f2937', lineHeight: 20 },
  profileFocus: { color: '#475569', marginTop: 6, fontWeight: '700' },
  legalBox: { backgroundColor: '#fffaf0', borderRadius: 8, padding: 12, borderWidth: 1, borderColor: '#ead7a1', marginTop: 14 },
  legalTitle: { color: '#7a5a12', fontWeight: '900', marginBottom: 6 },
  legalDescription: { color: '#4b5563', lineHeight: 19, marginBottom: 10 },
  legalLinkRow: { paddingVertical: 4, marginBottom: 4 },
  legalLinkText: { color: '#7a5a12', fontWeight: '800' },
  checkboxRow: { flexDirection: 'row', alignItems: 'flex-start', marginTop: 8 },
  checkbox: { width: 20, height: 20, borderRadius: 4, borderWidth: 1, borderColor: '#b8c1cc', backgroundColor: '#fff', marginRight: 10, alignItems: 'center', justifyContent: 'center', marginTop: 1 },
  checkboxChecked: { backgroundColor: '#111', borderColor: '#111' },
  checkboxCheck: { color: '#d4af37', fontWeight: '900', fontSize: 12 },
  checkboxText: { flex: 1, color: '#475569', lineHeight: 19, fontSize: 13 },
  actions: { marginBottom: 16 },
  videoHintBox: { backgroundColor: '#fff8e8', borderRadius: 8, borderWidth: 1, borderColor: '#ead7a1', padding: 12, marginBottom: 10 },
  videoHintTitle: { color: '#7a5a12', fontWeight: '900', marginBottom: 4 },
  videoHintText: { color: '#4b5563', lineHeight: 19 },
  videoHintMeta: { color: '#7a5a12', marginTop: 8, fontWeight: '800' },
  videoMetaBox: { backgroundColor: '#f8fafc', borderRadius: 8, borderWidth: 1, borderColor: '#dbe4ee', padding: 12, marginBottom: 10 },
  videoMetaText: { color: '#334155', lineHeight: 18, fontSize: 12 },
  secondaryButton: { minHeight: 48, borderRadius: 8, borderWidth: 1, borderColor: '#111', alignItems: 'center', justifyContent: 'center', marginBottom: 10, backgroundColor: '#fff' },
  secondaryButtonText: { color: '#111', fontWeight: '900' },
  secondaryButtonDark: { minHeight: 48, borderRadius: 8, borderWidth: 1, borderColor: '#d4af37', alignItems: 'center', justifyContent: 'center', marginTop: 8, backgroundColor: '#111' },
  secondaryButtonDarkText: { color: '#d4af37', fontWeight: '900' },
  primaryButton: { minHeight: 52, borderRadius: 8, backgroundColor: '#d4af37', alignItems: 'center', justifyContent: 'center', marginTop: 8 },
  primaryButtonText: { color: '#111', fontWeight: '900' },
  disabledButton: { opacity: 0.65 },
  resultPanel: { marginBottom: 14, backgroundColor: '#111', borderRadius: 8, padding: 16, borderWidth: 2, overflow: 'hidden' },
  tierStripe: { height: 8, marginHorizontal: -16, marginTop: -16, marginBottom: 14 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  cardName: { color: '#fff', fontSize: 22, fontWeight: '900' },
  cardMeta: { color: '#d4af37', fontWeight: '800', marginTop: 4 },
  cardTier: { color: '#fff', fontWeight: '800', marginTop: 4, fontSize: 12 },
  overall: { color: '#d4af37', fontSize: 56, fontWeight: '900' },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', marginTop: 12 },
  stat: { width: '50%', color: '#fff', fontWeight: '800', paddingVertical: 6 },
  deliveryBox: { backgroundColor: '#fff', borderRadius: 8, padding: 12, marginTop: 12, marginBottom: 8, borderWidth: 2 },
  deliveryTitle: { color: '#111', fontWeight: '900', marginBottom: 6 },
  deliverySectionTitle: { color: '#111', fontWeight: '900', marginTop: 8, marginBottom: 4 },
  deliveryText: { color: '#374151', marginBottom: 3 },
  deliveryNote: { color: '#6b7280', marginTop: 6, marginBottom: 6, fontSize: 12, lineHeight: 17 },
  trainingCycleBox: { marginTop: 8, marginBottom: 4, padding: 10, borderRadius: 8, borderWidth: 1, borderColor: '#e5e7eb', backgroundColor: '#f8fafc' },
  trainingCycleTitle: { color: '#111', fontWeight: '900', marginBottom: 4, fontSize: 12 },
  historyRow: { borderTopWidth: 1, borderTopColor: '#e5e7eb', paddingVertical: 10 },
  historyName: { color: '#111', fontWeight: '900' },
  historyMeta: { color: '#64748b', marginTop: 3, fontWeight: '700' }
});
