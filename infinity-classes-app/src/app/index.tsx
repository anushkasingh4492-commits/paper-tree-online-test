import React, { useState } from "react";
import { ActivityIndicator, StyleSheet, Text, View } from "react-native";
import { WebView } from "react-native-webview";

export default function HomeScreen() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  return (
    <View style={styles.container}>
      {loading && (
        <View style={styles.loading}>
          <ActivityIndicator size="large" />
          <Text style={styles.text}>Loading Infinity Classes...</Text>
        </View>
      )}

      {error ? (
        <View style={styles.error}>
          <Text style={styles.title}>Unable to load Infinity Classes</Text>
          <Text>{error}</Text>
        </View>
      ) : (
        <WebView
          source={{ uri: "https://web.infinityclasses.net" }}
          style={styles.webview}
          javaScriptEnabled
          domStorageEnabled
          sharedCookiesEnabled
          thirdPartyCookiesEnabled
          originWhitelist={["https://*"]}
          allowsBackForwardNavigationGestures
          automaticallyAdjustContentInsets={false}
          contentInsetAdjustmentBehavior="never"
          setSupportMultipleWindows={false}
          onLoadStart={() => {
            setLoading(true);
            setError("");
          }}
          onLoadEnd={() => {
            setLoading(false);
          }}
          onError={(event) => {
            console.log("WEBVIEW ERROR:", event.nativeEvent);
            setLoading(false);
            setError(
              event.nativeEvent.description ||
                "The website could not be loaded."
            );
          }}
          onHttpError={(event) => {
            console.log("WEBVIEW HTTP ERROR:", event.nativeEvent);
          }}
        />
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
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 12,
  },
});
