import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, Grid, CircularProgress, Alert } from '@mui/material';
import api from './api';

interface Case {
  id: number;
  status: string;
}

const Dashboard: React.FC = () => {
  const [total, setTotal] = useState(0);
  const [inProgress, setInProgress] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get<Case[] | { results: Case[] }>('/cases/')
      .then(res => {
        let cases: Case[] = [];
        if (Array.isArray(res.data)) {
          cases = res.data;
        } else if (Array.isArray((res.data as any).results)) {
          cases = (res.data as any).results;
        }
        setTotal(cases.length);
        setInProgress(cases.filter(c => c.status === 'InProgress').length);
        setCompleted(cases.filter(c => c.status === 'Completed').length);
        setError('');
        setLoading(false);
      })
      .catch(() => {
        setError('ダッシュボード情報の取得に失敗しました');
        setLoading(false);
      });
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>ダッシュボード</Typography>
        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}
        {!loading && !error && (
          <Grid container spacing={3}>
            {/* @ts-expect-error MUI v7型定義の不整合を一時的に抑制 */}
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6">全案件数</Typography>
                <Typography variant="h3">{total}</Typography>
              </Paper>
            </Grid>
            {/* @ts-expect-error MUI v7型定義の不整合を一時的に抑制 */}
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6">進行中</Typography>
                <Typography variant="h3">{inProgress}</Typography>
              </Paper>
            </Grid>
            {/* @ts-expect-error MUI v7型定義の不整合を一時的に抑制 */}
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6">完了</Typography>
                <Typography variant="h3">{completed}</Typography>
              </Paper>
            </Grid>
          </Grid>
        )}
      </Paper>
    </Container>
  );
};

export default Dashboard; 