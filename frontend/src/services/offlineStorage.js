/**
 * Offline Sync Service using browser IndexedDB.
 * Enables remote North-East field workers to submit hazard reports with photos offline.
 * Reports automatically synchronize once connectivity is restored.
 */

const DB_NAME = 'NER_Landslide_Offline_DB';
const DB_VERSION = 1;
const STORE_NAME = 'pending_reports';

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'idempotency_key' });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export const offlineStorage = {
  async saveReport(report) {
    const db = await openDB();
    const idempotency_key = report.idempotency_key || `offline_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    const record = {
      ...report,
      idempotency_key,
      sync_status: 'PENDING',
      created_at: new Date().toISOString(),
      retry_count: 0,
    };
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      store.put(record);
      tx.oncomplete = () => resolve(record);
      tx.onerror = () => reject(tx.error);
    });
  },

  async getPendingReports() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  },

  async removeReport(idempotency_key) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      store.delete(idempotency_key);
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => reject(tx.error);
    });
  }
};
