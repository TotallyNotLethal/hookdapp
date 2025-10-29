import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'fish.hookd.app',
  appName: 'Hookd',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
  plugins: {
    Camera: {
      webUseInput: true,
      resultType: 'uri',
      allowEditing: false,
      saveToGallery: false
    }
  }
};

export default config;
