import { Loader2 } from 'lucide-react';
import styles from './Loader.module.css';

const Loader = ({ size = 'medium', text = 'Loading...' }) => {
  const sizeMap = {
    small: 16,
    medium: 24,
    large: 36
  };

  return (
    <div className={styles.loaderContainer}>
      <Loader2 className={styles.spinner} size={sizeMap[size]} />
      {text && <p className={styles.text}>{text}</p>}
    </div>
  );
};

export default Loader;
