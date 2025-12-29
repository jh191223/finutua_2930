import React, { useState } from 'react';
import { View, Button, Image, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { photoAPI } from '../services/api';

export default function PhotoUploadScreen({ navigation }) {
  const [image, setImage] = useState(null);
  const [uploading, setUploading] = useState(false);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [3, 4],
      quality: 0.8,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  const uploadImage = async () => {
    if (!image) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: image,
        type: 'image/jpeg',
        name: 'photo.jpg',
      });

      const response = await photoAPI.upload(formData);
      Alert.alert('Success', '사진이 업로드되었습니다!');
      navigation.navigate('Avatar', { photoId: response.data.photo_id });
    } catch (error) {
      Alert.alert('Error', '업로드 실패: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      {image && <Image source={{ uri: image }} style={styles.image} />}
      <Button title="갤러리에서 선택" onPress={pickImage} />
      <Button 
        title={uploading ? "업로드 중..." : "업로드"} 
        onPress={uploadImage} 
        disabled={!image || uploading}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  image: {
    width: 300,
    height: 400,
    marginBottom: 20,
    borderRadius: 10,
  },
