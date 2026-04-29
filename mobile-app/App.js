import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  const [athlete, setAthlete] = useState({ name: '', age: '', position: '' });
  const [videoUri, setVideoUri] = useState(null);
  const [result, setResult] = useState(null);

  async function pickVideo() {
    const selected = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      quality: 1
    });

    if (!selected.canceled) {
      setVideoUri(selected.assets[0].uri);
    }
  }

  async function simulateAnalysis() {
    if (!athlete.name || !athlete.age || !athlete.position || !videoUri) {
      Alert.alert('Atenção', 'Preencha os dados e selecione um vídeo.');
      return;
    }

    const analysis = {
      overall: 74,
      speed: 78,
      technique: 72,
      gameIq: 70,
      physical: 76,
      potential: 82
    };

    setResult(analysis);
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>HUB-PODIUM</Text>
      <Text style={styles.subtitle}>Análise Inteligente de Atleta</Text>

      <TextInput style={styles.input} placeholder="Nome do atleta" value={athlete.name} onChangeText={(v) => setAthlete({ ...athlete, name: v })} />
      <TextInput style={styles.input} placeholder="Idade" keyboardType="numeric" value={athlete.age} onChangeText={(v) => setAthlete({ ...athlete, age: v })} />
      <TextInput style={styles.input} placeholder="Posição" value={athlete.position} onChangeText={(v) => setAthlete({ ...athlete, position: v })} />

      <Button title="Selecionar vídeo" onPress={pickVideo} />
      {videoUri && <Text style={styles.ok}>Vídeo selecionado</Text>}

      <View style={styles.space} />
      <Button title="Gerar análise R$49" onPress={simulateAnalysis} />

      {result && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>{athlete.name}</Text>
          <Text style={styles.overall}>{result.overall}</Text>
          <Text>POS: {athlete.position}</Text>
          <Text>VEL: {result.speed}</Text>
          <Text>TEC: {result.technique}</Text>
          <Text>QI JOGO: {result.gameIq}</Text>
          <Text>FÍSICO: {result.physical}</Text>
          <Text>POTENCIAL: {result.potential}</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: '#f6f2e8' },
  title: { fontSize: 32, fontWeight: 'bold', marginTop: 24 },
  subtitle: { fontSize: 18, marginBottom: 24 },
  input: { backgroundColor: '#fff', padding: 14, marginBottom: 12, borderRadius: 8, borderWidth: 1, borderColor: '#ddd' },
  ok: { marginTop: 8, color: 'green' },
  space: { height: 16 },
  card: { marginTop: 24, padding: 20, borderRadius: 16, backgroundColor: '#d4af37', alignItems: 'center' },
  cardTitle: { fontSize: 24, fontWeight: 'bold' },
  overall: { fontSize: 54, fontWeight: 'bold' }
});
