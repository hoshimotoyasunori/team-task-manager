import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, CircularProgress, Alert, List, ListItem, ListItemText } from '@mui/material';
import { useParams } from 'react-router-dom';
import api from './api';

interface CaseDetailType {
  id: number;
  case_type: string;
  status: string;
  occurence_date: string;
  property: number;
  owner: number;
  assigned_sales: number | null;
  created_at: string;
  updated_at: string;
  expected_construction_types: number[];
}

const CaseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [caseDetail, setCaseDetail] = useState<CaseDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    api.get<CaseDetailType>(`/cases/${id}/`)
      .then(res => {
        setCaseDetail(res.data);
        setError('');
      })
      .catch(() => {
        setError('案件詳細の取得に失敗しました');
      })
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>案件詳細</Typography>
        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}
        {!loading && !error && caseDetail && (
          <List>
            <ListItem><ListItemText primary={`ID: ${caseDetail.id}`} /></ListItem>
            <ListItem><ListItemText primary={`案件種別: ${caseDetail.case_type}`} /></ListItem>
            <ListItem><ListItemText primary={`ステータス: ${caseDetail.status}`} /></ListItem>
            <ListItem><ListItemText primary={`発生日: ${caseDetail.occurence_date}`} /></ListItem>
            <ListItem><ListItemText primary={`物件ID: ${caseDetail.property}`} /></ListItem>
            <ListItem><ListItemText primary={`オーナーID: ${caseDetail.owner}`} /></ListItem>
            <ListItem><ListItemText primary={`担当営業ID: ${caseDetail.assigned_sales ?? '未割当'}`} /></ListItem>
            <ListItem><ListItemText primary={`想定工事種別ID: ${caseDetail.expected_construction_types.join(', ')}`} /></ListItem>
            <ListItem><ListItemText primary={`登録日: ${caseDetail.created_at}`} /></ListItem>
            <ListItem><ListItemText primary={`更新日: ${caseDetail.updated_at}`} /></ListItem>
          </List>
        )}
      </Paper>
    </Container>
  );
};

export default CaseDetail; 