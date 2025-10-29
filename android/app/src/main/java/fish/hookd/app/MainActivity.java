package fish.hookd.app;

import android.os.Bundle;
import android.webkit.WebSettings;

import com.capacitorjs.plugins.camera.CameraPlugin;
import com.capacitorjs.plugins.filesystem.FilesystemPlugin;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.BridgeWebView;

public class MainActivity extends BridgeActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    // Ensure the Camera and Filesystem plugins are available to the WebView bridge.
    registerPlugin(CameraPlugin.class);
    registerPlugin(FilesystemPlugin.class);

    super.onCreate(savedInstanceState);

    BridgeWebView bridgeWebView = getBridge().getWebView();
    if (bridgeWebView != null) {
      WebSettings settings = bridgeWebView.getSettings();
      settings.setAllowFileAccess(true);
      settings.setAllowContentAccess(true);
      settings.setAllowFileAccessFromFileURLs(true);
      settings.setAllowUniversalAccessFromFileURLs(true);
    }
  }
}
