import React, { useEffect, useRef, useState } from "react";
import { ActivityIndicator, Platform, StyleSheet, Text, View } from "react-native";
import { WebView } from "react-native-webview";

const WEB_URL = "https://web.infinityclasses.net";

export default function HomeScreen() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const loadingTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearLoadingTimer = () => {
    if (loadingTimer.current) {
      clearTimeout(loadingTimer.current);
      loadingTimer.current = null;
    }
  };

  const finishLoading = () => {
    clearLoadingTimer();
    setLoading(false);
  };

  const startLoading = () => {
    clearLoadingTimer();
    setLoading(true);
    setError("");

    // Some SPA/redirect flows can keep Android WebView's load event open
    // even though the page is already usable. Never leave the user behind
    // an infinite native spinner.
    loadingTimer.current = setTimeout(() => {
      setLoading(false);
    }, 10000);
  };

  useEffect(() => {
    return () => clearLoadingTimer();
  }, []);

  return (
    <View style={styles.container}>
      {error ? (
        <View style={styles.error}>
          <Text style={styles.title}>Unable to load Infinity Classes</Text>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      ) : (
        <WebView
          source={{ uri: WEB_URL }}
          style={styles.webview}
          javaScriptEnabled
          domStorageEnabled
          cacheEnabled={false}
          cacheMode={Platform.OS === "android" ? "LOAD_NO_CACHE" : undefined}
          incognito={false}
          sharedCookiesEnabled
          thirdPartyCookiesEnabled
          setSupportMultipleWindows={false}
          originWhitelist={["https://*", "http://*"]}
          allowsBackForwardNavigationGestures
          automaticallyAdjustContentInsets={false}
          contentInsetAdjustmentBehavior="never"
          startInLoadingState={false}
          onLoadStart={startLoading}
          onLoadEnd={finishLoading}
          onLoadProgress={({ nativeEvent }) => {
            if (nativeEvent.progress >= 0.85) {
              finishLoading();
            }
          }}
          onNavigationStateChange={(navState) => {
            // A successful login/redirect can be a client-side navigation,
            // so don't keep the native spinner over the new dashboard.
            if (navState.url && navState.url !== WEB_URL) {
              finishLoading();
            }
          }}
          onError={(event) => {
            console.log("WEBVIEW ERROR:", event.nativeEvent);
            clearLoadingTimer();
            setLoading(false);
            setError(
              event.nativeEvent.description ||
                "The website could not be loaded."
            );
          }}
          onHttpError={(event) => {
            console.log("WEBVIEW HTTP ERROR:", event.nativeEvent);
            if (event.nativeEvent.statusCode >= 400) {
              finishLoading();
            }
          }}
        />
      )}

      {loading && !error && (
        <View style={styles.loading} pointerEvents="none">
          <ActivityIndicator size="large" />
          <Text style={styles.text}>Loading Infinity Classes...</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  webview: {
    flex: 1,
  },
  loading: {
    ...StyleSheet.absoluteFill,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#fff",
    zIndex: 10,
  },
  text: {
    marginTop: 12,
    fontSize: 16,
  },
  error: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 12,
  },
  errorText: {
    textAlign: "center",
  },
});
