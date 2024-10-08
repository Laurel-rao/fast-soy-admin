<script setup lang="tsx">
import { NButton, NTag } from 'naive-ui';
import {fetchBatchDeleteMenu, fetchGetMessageList} from '@/service/api';
import { useAppStore } from '@/store/modules/app';
import { useTable, useTableOperate } from '@/hooks/common/table';
import { $t } from '@/locales';
import { enableStatusRecord } from '@/constants/business';
import {useBoolean} from "~/packages/hooks";
import MessageOperateModal, {OperateType} from "@/views/manage/message/modules/message-operate-modal.vue";
import {ref} from "vue";

const appStore = useAppStore();

const { columns, columnChecks, data, loading, getData, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchGetMessageList,
  apiParams: {
    current: 1,
    size: 10
  },
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      width: 64,
      align: 'center'
    },
    {
      key: 'image',
      title: $t('page.manage.message.image'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'content',
      title: $t('page.manage.message.content'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'channelId',
      title: $t('page.manage.message.channelId'),
      align: 'center',
      minWidth: 120
    },
    {
      key: 'status',
      title: $t('page.manage.message.status'),
      align: 'center',
      width: 100,
      render: row => {
        if (row.status === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          1: 'success',
          2: 'warning'
        };

        const label = $t(enableStatusRecord[row.status]);

        return <NTag type={tagMap[row.status]}>{label}</NTag>;
      }
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => handleUpdate(row)}>
            {$t('common.edit')}
          </NButton>
        </div>
      )
    }
  ]
});

const {
  checkedRowKeys,
  // closeDrawer
} = useTableOperate(data, getData);
const { bool: visible, setTrue: openModal } = useBoolean();
const operateType = ref<OperateType>('add');
const curData = ref<any>();
function handleAdd() {
  operateType.value = 'add';
  openModal();
}

function handleUpdate(row: Api.Message.Message) {
  operateType.value = 'edit';
  curData.value = row;
  openModal();
}

async function handleBatchDelete() {
  // request
  const { error } = await fetchBatchDeleteMenu({ ids: checkedRowKeys.value });
  if (!error) {
    onBatchDeleted();
  }
}

</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NCard :title="$t('page.manage.message.title')" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          @add="handleAdd"
          @delete="handleBatchDelete"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="702"
        :loading="loading"
        remote
        :row-key="row => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
      <MessageOperateModal
        v-model:visible="visible"
        :operate-type="operateType"
        :cur-data="curData"
        @submitted="getData"
      />
    </NCard>

  </div>
</template>

<style scoped></style>
