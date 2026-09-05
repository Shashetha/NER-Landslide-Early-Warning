import styles from './StatCard.module.css';

const StatCard = ({ title, value, icon: Icon, trend, color = 'blue' }) => {
  return (
    <div className={`${styles.card} ${styles[color]}`}>
      <div className={styles.content}>
        <span className={styles.title}>{title}</span>
        <div className={styles.valueRow}>
          <span className={styles.value}>{value}</span>
          {trend && (
            <span className={`${styles.trend} ${trend > 0 ? styles.positive : styles.negative}`}>
              {trend > 0 ? '+' : ''}{trend}%
            </span>
          )}
        </div>
      </div>
      <div className={styles.iconWrapper}>
        <Icon size={24} />
      </div>
    </div>
  );
};

export default StatCard;
