# 重构方法库

scan 阶段匹配候选优化点的方法表，design 阶段每个执行步骤要引用一个方法号。

**方法号 `M-L{层}-{序号}`**。四层：

- **L1 行为等价迁移**——大改动有风险时把“改”拆成多步安全动作，详见 `methods-L1-L2.md`
- **L2 代码级重构**——Fowler 经典单次动作，单函数 / 局部改写，详见 `methods-L1-L2.md`
- **L3 结构拆分**——组件 / 模块 / 层级级别，详见 `methods-L3.md`
- **L4 性能与异步**——行为等价但运行特征变，详见 `methods-L4.md`

**统一字段**：适用 / 不适用 / 步骤 / 风险点 / 验证 / 前后端 / 配哪种 scan 项。前后端适用性大部分通用，特化的会在字段里标注。

## 方法号速查

### L1 行为等价迁移

- M-L1-01 Parallel Change 并行变更
- M-L1-02 Strangler Fig 绞杀者模式
- M-L1-03 Branch by Abstraction 分支抽象
- M-L1-04 Characterization Test 刻画测试

### L2 代码级重构

- M-L2-01 Extract Function 提取函数
- M-L2-02 Inline Function 内联函数
- M-L2-03 Extract Variable / Replace Temp with Query 提取变量 / 以查询取代临时变量
- M-L2-04 Move Function 搬移函数
- M-L2-05 Decompose Conditional 分解条件
- M-L2-06 Replace Conditional with Polymorphism 以多态取代条件
- M-L2-07 Introduce Parameter Object 引入参数对象
- M-L2-08 Replace Nested Conditional with Guard Clauses 守卫语句

### L3 结构拆分

- M-L3-01 Component Split 组件拆分（容器 / 展示）
- M-L3-02 Extract Composable / Custom Hook 抽取组合式函数
- M-L3-03 State Lifting / Lowering 状态提升 / 下沉
- M-L3-04 Service Layer Extraction 服务层抽取
- M-L3-05 Repository Extraction 仓储层抽取
- M-L3-06 Layer Rectification 分层纠偏
- M-L3-07 Single Responsibility Split 职责分离

### L4 性能与异步

- M-L4-01 Memoization 记忆化
- M-L4-02 Batching 批处理
- M-L4-03 Lazy Loading / Code Splitting 懒加载 / 代码分割
- M-L4-04 N+1 Query Elimination N+1 查询消除
- M-L4-05 Index & Cache 索引与缓存
- M-L4-06 Async & Cancellation 异步与取消
- M-L4-07 List Virtualization 列表虚拟化

## 用法速查

- **scan 阶段**：先用本文件按层级和方法号定位候选，再按需打开对应拆分文件读取完整字段。
- **design 阶段**：执行步骤引用方法号后，把对应拆分文件里的“步骤”字段落到本项目的具体文件 / 函数。方法库的步骤是骨架不是直接复制的答案。
- **扩展方法库**：新方法号接着层内编号递增。新增完整填齐所有字段——缺字段不准入库。
